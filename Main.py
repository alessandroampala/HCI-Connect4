from PyQt5 import QtWidgets
import sys
import layoutpython.MenuGui as Menu_Gui

# Starts the main menu window if Main.py file is called directly
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Menu_Gui.MenuGui(app.primaryScreen().size())
    app.exec_()
