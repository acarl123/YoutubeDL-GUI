import wx
from mainController import Controller


def main():
	app = wx.App(None)
	controller = Controller()
	controller.show()
	app.MainLoop()

if __name__ == '__main__':
	main()