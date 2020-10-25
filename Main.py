from PyQt5 import QtWidgets
import sys
import layoutpython.MenuGui as Menu

app = QtWidgets.QApplication(sys.argv)
window = Menu.MenuGui()
app.exec_()
