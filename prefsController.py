import wx
import os

from prefsView import PrefsDialog

ID3_TAGS = [
    'ARTIST',
    'GENRE',
    # 'ALBUM',
    # 'BPM'
]

class PrefsController:
    def __init__(self, parent):
        self.mainWindow = PrefsDialog(parent.mainWindow)

        # bind events
        self.mainWindow.Bind(wx.EVT_CHECKBOX, self.onOrgCheck, self.mainWindow.chkDir)
        self.mainWindow.Bind(wx.EVT_DIRPICKER_CHANGED, self.onDirChange, self.mainWindow.dirPickerSave)

        self.prefs = parent.prefs
        self.loadConfig()

    def showModal(self):
        return self.mainWindow.ShowModal()

    def onDirChange(self, event):
        self.prefs['defaultdir'] = self.mainWindow.dirPickerSave.GetPath()

    def loadConfig(self):
        # setup view
        self.mainWindow.chkDir.SetValue(self.prefs.get('makedirs'))
        self.mainWindow.dirPickerSave.SetPath(self.prefs.get('defaultdir'))

    def onOrgCheck(self, event):
        self.prefs['makedirs'] = self.mainWindow.chkDir.GetValue()
