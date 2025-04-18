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
        self.mainWindow.Bind(wx.EVT_BUTTON, self.onLoadAll, self.mainWindow.btnLoadAll)
        
        # set display
        self.mainWindow.btnLoadAll.Disable()

        self.download_queue = []
        self.total_cnt = 0
        self.queue_cnt = 0
        self.cur_url = ''
        self.futures = []
        self.executor = ThreadPoolExecutor(max_workers=self.WORKER_LIMIT)
        
    def showModel(self):
        # stops tasks in the queue
        return self.mainWindow.ShowModal()

    def onClose(self, *args, **kwargs):
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
            self.update_count()
            self.display_result()
            self.mainWindow.btnLoadAll.Enable()
            self.mainWindow.btnLoad.Disable()
    
    def onLoadAll(self, event):
        self.disable_window()
        # add 1st one already loaded
        self.download_queue.append({
            'artist': self.mainWindow.txtArtist.GetValue().strip(),
            'title': self.mainWindow.txtTitle.GetValue().strip(),
            'genre': self.mainWindow.txtGenre.GetValue().strip(),
            'url': self.cur_url
        })
        self.queue_cnt += 1
        self.mainWindow.lstQueue.AppendItems([f'{self.mainWindow.txtTitle.GetValue().strip()} - {self.mainWindow.txtArtist.GetValue().strip()}'])
        self.mainWindow.lstQueue.Refresh()
        
        while self.futures:
            self.update_count()
            res = self.futures.pop(0).result()
            if res.get('errors'):
                print(res.get('errors'))
                continue
            
            self.cur_url = res.get('url')
            self.download_queue.append({
            'artist': res.get('artist').strip(),
            'title': res.get('title').strip(),
            'genre': self.mainWindow.txtGenre.GetValue().strip(),
            'url': res.get('url')
            })
            self.queue_cnt += 1
            self.mainWindow.lstQueue.AppendItems([f"{res.get('title').strip()} - {res.get('artist').strip()}"])
            self.mainWindow.lstQueue.Refresh()
            self.mainWindow.Layout()
        
        self.enable_window()
        self.mainWindow.btnAdd.Disable()
        self.mainWindow.btnSkip.Disable()
        self.mainWindow.btnLoadAll.Disable()
    
    def update_count(self):
        self.mainWindow.lblCnt.SetLabelText(f'{self.queue_cnt}/{self.total_cnt}')
    
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
        self.queue_cnt += 1
        self.mainWindow.lstQueue.AppendItems([f'{self.mainWindow.txtTitle.GetValue().strip()} - {self.mainWindow.txtArtist.GetValue().strip()}'])
        self.mainWindow.lstQueue.Refresh()
        
        # check if we have all of the results, and disable controls if so
        if not self.futures:
            self.mainWindow.btnAdd.Disable()
            self.mainWindow.btnSkip.Disable()
            self.mainWindow.btnLoadAll.Disable()
        else:
            self.display_result()
        
    def _parse_csv(self, csv_file):
        with open(csv_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.total_cnt += 1
                self.futures.append(self.executor.submit(self._do_search, search_terms={
                    'artist': row.get('Artist Name(s)'),
                    'title': row.get('Track Name')
                }))

    def disable_window(self):
        self.mainWindow.SetCursor(wx.Cursor(wx.CURSOR_WAIT))
        self.mainWindow.btnAdd.Disable()
        self.mainWindow.btnSkip.Disable()
        self.mainWindow.btnLoadAll.Disable()
        self.mainWindow.Layout()
    
    def enable_window(self):
        # set view back to original state
        self.mainWindow.SetCursor(wx.Cursor())
        self.mainWindow.btnAdd.Enable()
        self.mainWindow.btnSkip.Enable()
        self.mainWindow.btnLoadAll.Enable()
        self.mainWindow.Layout()
    
    def display_result(self):
        self.update_count()
        self.disable_window()  
        res = self.futures.pop(0).result()
        self.enable_window()
        
        # check if no errors
        # TODO: show errors in dialog
        if res.get('errors'):
            print(res.get('errors'))
            self.display_result()
            return
        
        # set up view
        self.mainWindow.txtArtist.SetValue(res.get('artist'))
        self.mainWindow.txtTitle.SetValue(res.get('title'))
        self.mainWindow.btnNext.Disable()
        self.mainWindow.btnPrevious.Disable()
        
        if res.get('thumbnail'):
            image = wx.Image(io.BytesIO(res.get('thumbnail')))
            image = image.Scale(self.mainWindow.mThumbnail.Size[0], self.mainWindow.mThumbnail.Size[1], wx.IMAGE_QUALITY_HIGH)
            self.mainWindow.mThumbnail.SetBitmap(wx.BitmapBundle(image))
            self.mainWindow.mThumbnail.Refresh()
        self.mainWindow.lblVideo.SetLabelText(f"{res.get('title')} - {res.get('channel')}")
        self.mainWindow.lblVideo.Refresh()
        self.cur_url = res.get('url')
            
    def _do_search(self, search_terms):
        output_dict = {}
        artist = search_terms.get('artist')
        output_dict['artist'] = artist
        title = search_terms.get('title')
        output_dict['title'] = title
        
        with yt_dlp.YoutubeDL() as ydl:
            try:
                results = ydl.extract_info(f'ytsearch:{title} - {artist}', download=False)['entries'][0:5]
                # TODO: able to page through multiple search results
                if not results:
                    output_dict['error'] = 'no results returned'
                    return output_dict
                result = results[0]
            except Exception as e:
                output_dict['error'] = e
                return output_dict
            
            thumbnail = [thumb.get('url') for thumb in result.get('thumbnails') if int(thumb.get('height', 0)) >= 100 and thumb.get('url')[-3:] == 'jpg']
            if thumbnail:
                data = requests.get(thumbnail[0])
                output_dict['thumbnail'] = data.content
                
            output_dict['url'] = result.get('webpage_url')
            output_dict['channel'] = result.get('channel')
            return output_dict
