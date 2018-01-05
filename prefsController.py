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
		self.mainWindow.Bind(wx.EVT_CHOICE, self.onFieldChoice, self.mainWindow.choiceDir)

		self.prefs = parent.prefs
		self.loadConfig()

	def showModal(self):
		return self.mainWindow.ShowModal()

	def onDirChange(self, event):
		self.prefs['defaultdir'] = self.mainWindow.dirPickerSave.GetPath()

	def onFieldChoice(self, event):
		self.prefs['autodirfield'] = self.mainWindow.choiceDir.GetString(self.mainWindow.choiceDir.GetCurrentSelection())

	def loadConfig(self):
		# setup view
		for sortTag in ID3_TAGS: self.mainWindow.choiceDir.Append(sortTag)	
		self.mainWindow.chkDir.SetValue(self.prefs.get('makedirs'))
		self.mainWindow.dirPickerSave.SetPath(self.prefs.get('defaultdir'))
		self.mainWindow.choiceDir.SetSelection(self.mainWindow.choiceDir.FindString(self.prefs.get('autodirfield'), caseSensitive=False))

		if not self.mainWindow.chkDir.GetValue():
			self.mainWindow.lblDir.Show(False)
			self.mainWindow.choiceDir.Show(False)
			self.mainWindow.Layout()

	def onOrgCheck(self, event):
		self.mainWindow.choiceDir.Show(self.mainWindow.chkDir.GetValue())
		self.mainWindow.lblDir.Show(self.mainWindow.chkDir.GetValue())
		self.mainWindow.Layout()

		self.prefs['makedirs'] = self.mainWindow.chkDir.GetValue()