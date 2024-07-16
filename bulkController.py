import wx
import csv
import os
import io
import yt_dlp
import requests
import threading
from concurrent.futures import ThreadPoolExecutor

from bulkView import bulkDialog

class BulkController:
    
    WORKER_LIMIT = 4
    
    def __init__(self, parent):
        wx.InitAllImageHandlers()
        self.mainWindow = bulkDialog(parent.mainWindow)
        
        # bind events
        self.mainWindow.Bind(wx.EVT_BUTTON, self.onLoad, self.mainWindow.btnLoad)
        self.mainWindow.Bind(wx.EVT_BUTTON, self.onSkip, self.mainWindow.btnSkip)
        self.mainWindow.Bind(wx.EVT_BUTTON, self.onAdd, self.mainWindow.btnAdd)
        self.mainWindow.Bind(wx.EVT_BUTTON, self.onFinish, self.mainWindow.btnFinish)
        self.mainWindow.Bind(wx.EVT_BUTTON, self.onCancel, self.mainWindow.btnCancel)
        self.mainWindow.Bind(wx.EVT_CLOSE, self.onClose, self.mainWindow)

        self.download_queue = []
        self.cur_url = ''
        self.futures = []
        self.executor = ThreadPoolExecutor(max_workers=self.WORKER_LIMIT)
        
    def showModel(self):
        # stops tasks in the queue
        return self.mainWindow.ShowModal()

    def onClose(self):
        self.executor.shutdown()
    
    def onLoad(self, event):
        file_picker = wx.FileDialog(self.mainWindow,
                                    defaultDir=os.path.expanduser('~'),
                                    message='Select CSV file from Exportify to load',
                                    wildcard='CSV files (*.csv)|*.csv')
        if file_picker.ShowModal() == wx.ID_OK:
            csv_file = file_picker.GetPath()
            self._parse_csv(csv_file)
            
            # call to update ui
            self.display_result()
    
    def onFinish(self, event):
        self.mainWindow.EndModal(wx.ID_OK)
        self.mainWindow.Destroy()
    
    def onCancel(self, event):
        self.mainWindow.EndModal(wx.ID_CANCEL)
        self.mainWindow.Destroy()
        
    def onSkip(self, event):
        # check if we have all of the results, and disable controls if so
        if not self.futures:
            self.mainWindow.btnAdd.Disable()
            self.mainWindow.btnSkip.Disable()
        else:
            self.display_result()
    
    def onAdd(self, event):
        self.download_queue.append({
            'artist': self.mainWindow.txtArtist.GetValue().strip(),
            'title': self.mainWindow.txtTitle.GetValue().strip(),
            'genre': self.mainWindow.txtGenre.GetValue().strip(),
            'url': self.cur_url
        })
        self.mainWindow.lstQueue.AppendItems([f'{self.mainWindow.txtTitle.GetValue().strip()} - {self.mainWindow.txtArtist.GetValue().strip()}'])
        self.mainWindow.lstQueue.Refresh()
        
        # check if we have all of the results, and disable controls if so
        if not self.futures:
            self.mainWindow.btnAdd.Disable()
            self.mainWindow.btnSkip.Disable()
        else:
            self.display_result()
        
    def _parse_csv(self, csv_file):
        with open(csv_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.futures.append(self.executor.submit(self._do_search, search_terms={
                    'artist': row.get('Artist Name(s)'),
                    'title': row.get('Track Name')
                }))

    def disable_window(self):
        self.mainWindow.SetCursor(wx.Cursor(wx.CURSOR_WAIT))
        for widget in self.mainWindow.GetChildren():
            widget.Disable()
    
    def enable_window(self):
        # set view back to original state
        self.mainWindow.SetCursor(wx.Cursor())
        for widget in self.mainWindow.GetChildren():
            widget.Enable()
    
    def display_result(self):
        self.disable_window()  
        res = self.futures.pop(0).result()
        self.enable_window()
        
        # set up view
        self.mainWindow.txtArtist.SetValue(res.get('artist'))
        self.mainWindow.txtTitle.SetValue(res.get('title'))
        self.mainWindow.btnNext.Disable()
        self.mainWindow.btnPrevious.Disable()
        
        if res.get('thumbnail'):
            image = wx.Image(io.BytesIO(res.get('thumbnail')))
            image = image.Scale(self.mainWindow.mThumbnail.Size[0], self.mainWindow.mThumbnail.Size[1], wx.IMAGE_QUALITY_HIGH)
            self.mainWindow.mThumbnail.SetBitmap(wx.BitmapBundle(image))
        self.mainWindow.lblVideo.SetLabelText(f"{res['title']} - {res['channel']}")
        self.cur_url = res.get('url')
            
    def _do_search(self, search_terms):
        output_dict = {}
        artist = search_terms.get('artist')
        output_dict['artist'] = artist
        title = search_terms.get('title')
        output_dict['title'] = title
        
        with yt_dlp.YoutubeDL() as ydl:
            results = ydl.extract_info(f'ytsearch:{title} - {artist}', download=False)['entries'][0:5]
            # TODO: able to page through multiple search results
            result = results[0]
            thumbnail = [thumb.get('url') for thumb in result.get('thumbnails') if int(thumb.get('height', 0)) >= 100 and thumb.get('url')[-3:] == 'jpg']
            if thumbnail:
                data = requests.get(thumbnail[0])
                output_dict['thumbnail'] = data.content
                
            output_dict['url'] = result.get('webpage_url')
            output_dict['channel'] = result.get('channel')
            return output_dict
