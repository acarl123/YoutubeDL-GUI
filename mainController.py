from mainView import MainFrame
from threading import Thread
from wx.lib.pubsub import pub as Publisher
from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH

import wx
import youtube_dl
import re


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
			}
		self.videoURL = ''
		self.parent = parent
		self.func = None
		self.callafter = None
		self.daemon = True
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
			returns = self.func()
			wx.CallAfter(Publisher.sendMessage, "update", data={'callafter':self.callafter, 'returns': returns})
			self.func = self.callafter = None

	def _download(self):
		if not self.videoURL: return
		opts = self.opts
		with youtube_dl.YoutubeDL(opts) as ydl:
			ydl.download([self.videoURL])

	def _get_video_info(self):
		if not self.videoURL: return
		opts = {
			'simulate': True,
		}
		with youtube_dl.YoutubeDL(opts) as ydl:
			info_dict = ydl.extract_info(self.videoURL, download=False)

		return info_dict
	# ===================== Separate Thread Above ==================== #


class Controller:
	URL_REGEX = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE
        )
	TITLE_REGEX = re.compile(
		r'^(?P<artist>[0-9A-Za-z\'\"\ ]+)?\-?(?P<title>.+)'
		)

	def __init__(self):
		self.mainWindow = MainFrame(None)
		self.downloader = YoutubeDownloader(self)
		Publisher.subscribe(self._update_after_thread, "update")

		# bind events
		self.mainWindow.Bind(wx.EVT_BUTTON, self.onURLClick, self.mainWindow.btnGetInfo)
		self.mainWindow.Bind(wx.EVT_BUTTON, self.onDownloadClick, self.mainWindow.btnDownload)

		# setup view
		self.mainWindow.barStatus.SetStatusText('Ready')
		self.mainWindow.btnDownload.Disable()

	def show(self):
		self.mainWindow.Show()

	def onURLClick(self, event):
		# change mouse cursor
		self.mainWindow.SetCursor(wx.Cursor(wx.CURSOR_WAIT))

		self.mainWindow.barStatus.SetStatusText('Pulling Info...')
		self.mainWindow.txtArtist.Clear()
		self.mainWindow.txtTitle.Clear()
		videoURL = self._validate_url(self.mainWindow.txtURL.GetLineText(0))
		if not videoURL: return
		self.downloader.videoURL = videoURL
		self.downloader.get_video_info(callafter=self.finish_info_display)

	def finish_info_display(self, info_dict=None):
		self.mainWindow.barStatus.SetStatusText('Ready')
		if not info_dict:return
		artist, title = self._get_title_info(info_dict.get('title'))
		self.downloader.opts.update({'outtmpl': '{}-{}.%(ext)s'.format(artist.strip(), title.strip())})
		self.mainWindow.txtArtist.SetValue(artist.strip())
		self.mainWindow.txtTitle.SetValue(title.strip())

		# set cursor back
		self.mainWindow.SetCursor(wx.Cursor())

		self.mainWindow.btnDownload.Enable()

	def onDownloadClick(self, event):
		# change mouse cursor
		self.mainWindow.SetCursor(wx.Cursor(wx.CURSOR_WAIT))

		self.mainWindow.barStatus.SetStatusText('Downloading...')
		self.mainWindow.btnDownload.Disable()
		self.mainWindow.btnGetInfo.Disable()
		self.mainWindow.txtArtist.Disable()
		self.mainWindow.txtTitle.Disable()
		self.mainWindow.txtURL.Disable()
		self.downloader.download(callafter=self.finish_download)

	def finish_download(self, *args):
		# set id3 tags
		artist = self.mainWindow.txtArtist.GetValue()
		title = self.mainWindow.txtTitle.GetValue()
		mp3_file = MP3File('%s-%s.mp3' % (artist, title))
		mp3_file.artist = artist
		mp3_file.url = self.mainWindow.txtURL.GetValue()
		mp3_file.song = title
		mp3_file.save()

		# set cursor back
		self.mainWindow.SetCursor(wx.Cursor())

		self.mainWindow.barStatus.SetStatusText('Ready')
		self.mainWindow.btnGetInfo.Enable()
		self.mainWindow.txtArtist.Enable()
		self.mainWindow.txtTitle.Enable()
		self.mainWindow.txtURL.Enable()

	def update_prog_bar(self, value):
		if isinstance(value, str):
			self.mainWindow.barStatus.SetStatusText('Download Complete, Converting...')
		else:
			if value > 100: 
				return
			else:
				self.mainWindow.barStatus.SetStatusText('Downloading(%s%%)...' % value)
				wx.Yield()

	def _get_title_info(self, title):
		matches = re.match(self.TITLE_REGEX, title)
		if not matches: return ('', title) # if the regex misses for some reason, put everything in title spot
		return (matches.group('artist'), matches.group('title'))

	def _validate_url(self, url):
		matches = re.match(self.URL_REGEX, url)
		if not matches: return
		return matches[0]

	def _update_after_thread(self, data):
		if isinstance(data, int):
			self.update_prog_bar(data)
		elif isinstance(data, str):
			self.update_prog_bar(data)
		else:
			data['callafter'](data.get('returns'))