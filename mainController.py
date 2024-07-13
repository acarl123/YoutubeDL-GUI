from mainView import MainFrame
from threading import Thread
from pubsub import pub as Publisher

import wx
import os
import yt_dlp
import re
import ast
import taglib
import configparser

from prefsController import PrefsController


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
            ydl.download([self.videoURL])

    def _get_video_info(self):
        if not self.videoURL: return
        opts = {
            'simulate': True,
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
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
        r'^(?P<artist>[0-9A-Za-z\[\]\&\.\'\"\ ]+)?\-?(?P<title>.+)'
        )

    def __init__(self):
        self.mainWindow = MainFrame(None)
        self.downloader = YoutubeDownloader(self)
        Publisher.subscribe(self._update_after_thread, "update")
        Publisher.subscribe(self._handle_error, "error")

        # bind events
        self.mainWindow.Bind(wx.EVT_BUTTON, self.onURLClick, self.mainWindow.btnGetInfo)
        self.mainWindow.Bind(wx.EVT_BUTTON, self.onDownloadClick, self.mainWindow.btnDownload)
        self.mainWindow.Bind(wx.EVT_MENU, self.onExit, self.mainWindow.menuQuit)
        self.mainWindow.Bind(wx.EVT_MENU, self.onPrefs, self.mainWindow.menuPrefs)
        self.mainWindow.Bind(wx.EVT_BUTTON, self.onSwap, self.mainWindow.btnSwap)

        # setup view
        self.mainWindow.barStatus.SetStatusText('Ready')
        self.mainWindow.btnDownload.Disable()
        self.mainWindow.SetWindowStyle(self.mainWindow.GetWindowStyle() ^ wx.RESIZE_BORDER) # disable resize

        # load confs
        self.prefs = {
            'makedirs': False,
            'autodirfield': '',
            'defaultdir': os.path.dirname(__file__)
        }
        self.loadConfig()
        self.setup_cmb_selection()

    def show(self):
        self.mainWindow.Show()

    def onExit(self, event):
        self.mainWindow.Destroy()
        exit(0)

    def loadConfig(self):
        config = configparser.ConfigParser()
        if os.path.isfile('config.ini'):
            config.read('config.ini')
            self.prefs = dict(config['DEFAULT'])
            # need to convert bools, need a better way to do this
            self.prefs['makedirs'] = config.getboolean('DEFAULT', 'makedirs')

    def setup_cmb_selection(self):
        # setup combobox choices based on current dir structure
        self.mainWindow.cmbGenre.Clear()
        subfolders = [f.name for f in os.scandir(self.prefs.get('defaultdir', os.getcwd())) if f.is_dir()]
        self.mainWindow.cmbGenre.AppendItems(sorted(subfolders))

    def onPrefs(self, event):
        prefsController = PrefsController(self)
        if prefsController.showModal() == wx.ID_OK:
            self.prefs = prefsController.prefs
            print(self.prefs)
            config = configparser.ConfigParser(strict=False)
            config['DEFAULT'] = self.prefs
            with open('config.ini', 'w') as configFile:
                config.write(configFile)

    def onSwap(self, event):
        title = self.mainWindow.txtTitle.GetValue()
        artist = self.mainWindow.txtArtist.GetValue()
        
        self.mainWindow.txtArtist.SetValue(title)
        self.mainWindow.txtTitle.SetValue(artist)
     
    def onURLClick(self, event):
        # change mouse cursor
        self.mainWindow.SetCursor(wx.Cursor(wx.CURSOR_WAIT))

        self.mainWindow.txtArtist.Clear()
        self.mainWindow.txtTitle.Clear()
        videoURL = self._validate_url(self.mainWindow.txtURL.GetLineText(0))
        if not videoURL: return
        self.disable_window()
        self.mainWindow.barStatus.SetStatusText('Pulling Info...')
        self.downloader.videoURL = videoURL
        self.downloader.get_video_info(callafter=self.finish_info_display)

    def finish_info_display(self, info_dict=None):
        self.mainWindow.barStatus.SetStatusText('Ready')
        if not info_dict:return
        artist, title = self._get_title_info(info_dict.get('title'))
        if artist: 
            artist = artist.strip()
        else:
            artist = ''
        if title: 
            title = title.strip()
        else:
            title = ''
        self.downloader.opts.update({'outtmpl': '{} - {}.%(ext)s'.format(artist, title)})
        self.mainWindow.txtArtist.SetValue(artist)
        self.mainWindow.txtTitle.SetValue(title)

        # set cursor back
        self.reset_window()

        self.mainWindow.btnDownload.Enable()

    def onDownloadClick(self, event):
        # change mouse cursor
        self.mainWindow.SetCursor(wx.Cursor(wx.CURSOR_WAIT))

        artist = self.mainWindow.txtArtist.GetValue()
        title = self.mainWindow.txtTitle.GetValue()
        self.downloader.opts.update({'outtmpl': '{} - {}.%(ext)s'.format(artist.strip(), title.strip())})
        self.mainWindow.barStatus.SetStatusText('Downloading...')
        self.disable_window
        self.downloader.download(callafter=self.finish_download)

    def finish_download(self, *args):
        # set id3 tags
        artist = self.mainWindow.txtArtist.GetValue().strip()
        title = self.mainWindow.txtTitle.GetValue().strip()
        genre = self.mainWindow.cmbGenre.GetValue().strip()
        try:
            mp3_file = taglib.File('%s - %s.mp3' % (artist, title))
            mp3_file.tags['ARTIST'] = [artist]
            mp3_file.tags['TITLE'] = title
            mp3_file.tags['GENRE'] = genre
            mp3_file.save()
            mp3_file.close()
        except OSError:
            self._handle_error('cannot open file for tag editing (possibly due to special characters).\nNot populating ID3 tags...')
            # self.reset_window()


        # move to new location
        if self.prefs.get('makedirs'):
            newDir = os.path.join(self.prefs.get('defaultdir'), genre)
            os.makedirs(newDir, exist_ok=True)
        else:
            newDir = self.prefs.get('defaultdir')

        filename = '{} - {}.mp3'.format(artist, title)
        try:
            os.rename(filename, os.path.join(newDir, filename))
        except Exception as e:
            self._handle_error(e)

        self.reset_window()

    def disable_window(self):
        for widget in self.mainWindow.GetChildren():
            widget.Disable()

    def reset_window(self):
        # set view back to original state
        self.mainWindow.SetCursor(wx.Cursor())
        self.mainWindow.barStatus.SetStatusText('Ready')
        for widget in self.mainWindow.GetChildren():
            widget.Enable()
        self.mainWindow.btnDownload.Disable()

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

    def _handle_error(self, data):
        msg_box = wx.MessageDialog(self.mainWindow, str(data), "Error handling youtube_dl", style=wx.OK|wx.CENTRE|wx.ICON_ERROR)
        msg_box.ShowModal()
        self.reset_window()