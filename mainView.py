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
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):
    
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 504,301 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )
        
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        
        bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Youtube URL", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        bSizer2.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.txtURL = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.txtURL, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.btnGetInfo = wx.Button( self, wx.ID_ANY, u"Get Info", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.btnGetInfo, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        
        bSizer1.Add( bSizer2, 0, wx.EXPAND, 5 )
        
        self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer1.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
        
        fgSizer4 = wx.FlexGridSizer( 0, 3, 0, 0 )
        fgSizer4.SetFlexibleDirection( wx.BOTH )
        fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Title", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )
        fgSizer4.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.txtTitle = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.txtTitle.SetMinSize( wx.Size( 400,-1 ) )
        
        fgSizer4.Add( self.txtTitle, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.btnSwap = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( u"assets/icons8-swap-24.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        
        # self.btnSwap.SetBitmapDisabled( wx.Bitmap( u"assets/icons8-swap-24.png", wx.BITMAP_TYPE_ANY ) )
        # self.btnSwap.SetBitmapSelected( wx.Bitmap( u"assets/icons8-swap-24.png", wx.BITMAP_TYPE_ANY ) )
        # self.btnSwap.SetBitmapFocus( wx.Bitmap( u"assets/icons8-swap-24.png", wx.BITMAP_TYPE_ANY ) )
        # self.btnSwap.SetBitmapHover( wx.Bitmap( u"assets/icons8-swap-24.png", wx.BITMAP_TYPE_ANY ) )
        self.btnSwap.SetToolTip( u"Swap artist and title" )
        
        fgSizer4.Add( self.btnSwap, 0, wx.ALL, 5 )
        
        self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Artist", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )
        fgSizer4.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.txtArtist = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.txtArtist.SetMinSize( wx.Size( 400,-1 ) )
        
        fgSizer4.Add( self.txtArtist, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        
        fgSizer4.Add( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u"Genre", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText8.Wrap( -1 )
        fgSizer4.Add( self.m_staticText8, 0, wx.ALL, 5 )
        
        cmbGenreChoices = []
        self.cmbGenre = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, cmbGenreChoices, 0 )
        fgSizer4.Add( self.cmbGenre, 0, wx.ALL|wx.EXPAND, 5 )
        
        
        bSizer1.Add( fgSizer4, 0, 0, 5 )
        
        self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer1.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )
        
        self.btnDownload = wx.Button( self, wx.ID_ANY, u"Download", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer1.Add( self.btnDownload, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        
        self.SetSizer( bSizer1 )
        self.Layout()
        self.barStatus = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
        self.m_menubar1 = wx.MenuBar( 0 )
        self.m_menu1 = wx.Menu()
        self.menuBulk = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Bulk Download from Exportify...", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu1.Append( self.menuBulk )
        
        self.menuPrefs = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Preferences...", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu1.Append( self.menuPrefs )
        
        self.m_menu1.AppendSeparator()
        
        self.menuQuit = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"&Quit", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu1.Append( self.menuQuit )
        
        self.m_menubar1.Append( self.m_menu1, u"&File" ) 
        
        self.SetMenuBar( self.m_menubar1 )
        
        
        self.Centre( wx.BOTH )
    
    def __del__( self ):
        pass
    

