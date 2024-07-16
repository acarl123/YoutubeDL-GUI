# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class bulkDialog
###########################################################################

class bulkDialog ( wx.Dialog ):
    
    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 698,507 ), style = wx.DEFAULT_DIALOG_STYLE )
        
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        
        bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.btnPrevious = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( u"assets/left-arrow.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        bSizer5.Add( self.btnPrevious, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        bSizer61 = wx.BoxSizer( wx.VERTICAL )
        
        self.lblVideo = wx.StaticText( self, wx.ID_ANY, u"Video Title - Channel Name", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.lblVideo.Wrap( -1 )
        bSizer61.Add( self.lblVideo, 0, wx.ALL|wx.ALIGN_LEFT, 5 )
        
        self.mThumbnail = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer61.Add( self.mThumbnail, 1, wx.ALL|wx.EXPAND, 5 )
        
        fgSizer1 = wx.FlexGridSizer( 2, 3, 0, 0 )
        fgSizer1.SetFlexibleDirection( wx.BOTH )
        fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Title", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )
        fgSizer1.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Artist", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )
        fgSizer1.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Genre", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )
        fgSizer1.Add( self.m_staticText4, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.txtTitle = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer1.Add( self.txtTitle, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.txtArtist = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer1.Add( self.txtArtist, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.txtGenre = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer1.Add( self.txtGenre, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        
        bSizer61.Add( fgSizer1, 0, wx.EXPAND, 5 )
        
        
        bSizer5.Add( bSizer61, 1, wx.EXPAND, 5 )
        
        self.btnNext = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( u"assets/right-arrow.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        bSizer5.Add( self.btnNext, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        bSizer8 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Queue", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        bSizer8.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        lstQueueChoices = []
        self.lstQueue = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, lstQueueChoices, 0 )
        bSizer8.Add( self.lstQueue, 1, wx.ALL|wx.EXPAND, 5 )
        
        
        bSizer5.Add( bSizer8, 1, wx.EXPAND, 5 )
        
        
        bSizer1.Add( bSizer5, 1, wx.EXPAND, 5 )
        
        bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
        
        
        bSizer6.Add( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.btnAdd = wx.Button( self, wx.ID_ANY, u"Add to Queue", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer6.Add( self.btnAdd, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.btnSkip = wx.Button( self, wx.ID_ANY, u"Skip", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer6.Add( self.btnSkip, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        
        bSizer6.Add( ( 0, 0), 3, wx.EXPAND, 5 )
        
        
        bSizer1.Add( bSizer6, 0, wx.EXPAND, 5 )
        
        self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer1.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )
        
        bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.btnLoad = wx.Button( self, wx.ID_ANY, u"Load CSV", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer7.Add( self.btnLoad, 0, wx.ALL, 5 )
        
        
        bSizer7.Add( ( 0, 0), 1, wx.EXPAND, 5 )
        
        
        bSizer7.Add( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.btnFinish = wx.Button( self, wx.ID_ANY, u"Finish and Download", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer7.Add( self.btnFinish, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.btnCancel = wx.Button( self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer7.Add( self.btnCancel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        
        bSizer1.Add( bSizer7, 0, wx.EXPAND, 5 )
        
        
        self.SetSizer( bSizer1 )
        self.Layout()
        
        self.Centre( wx.BOTH )
    
    def __del__( self ):
        pass
    

