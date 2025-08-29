import yt_dlp
import wx

from threading import Thread
from pubsub import pub as Publisher


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

class YoutubeDownloader(Thread):
    def __init__(self, parent=None):
        Thread.__init__(self)
        self.opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'logger': MyLogger(),
                'progress_hooks': [self._hook],
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        self.videoURL = ''
        self.parent = parent
        self.func = None
        self.callafter = None
        self.daemon = True
        self.search_terms = {}
        self.start()

    def _hook(self, d):
        if d['status'] == 'finished':
            Publisher.sendMessage("update", data='converting')
        elif d['status'] == 'downloading':
            if not d.get('total_bytes'):
                Publisher.sendMessage("update", data=101)
            else:
                Publisher.sendMessage("update", data=int((d.get('downloaded_bytes') / d.get('total_bytes')) * 100))

    def download(self, callafter=None):
        self.func = self._download
        self.callafter = callafter

    def get_video_info(self, callafter=None):
        self.func = self._get_video_info
        self.callafter = callafter
    
    # ===================== Separate Thread Below ==================== #
    def run(self):
        while True:
            if not self.func: continue
            try:
                returns = self.func()
                wx.CallAfter(Publisher.sendMessage, "update", data={'callafter':self.callafter, 'returns': returns})
            except Exception as e:
                Publisher.sendMessage("error", data=e)
            finally:
                self.func = self.callafter = None
        
    def _download(self):
        if not self.videoURL: return
        opts = self.opts
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(self.videoURL, download=True)
            # Copy info dict and change video extension to audio extension
            info_with_audio_extension = dict(info)
            info_with_audio_extension['ext'] = 'mp3'
            # Return filename with the correct extension
            return ydl.prepare_filename(info_with_audio_extension)

    def _get_video_info(self):
        if not self.videoURL: return
        opts = {
            'simulate': True,
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            info_dict = ydl.extract_info(self.videoURL, download=False)

        return info_dict
    # ===================== Separate Thread Above ==================== #

