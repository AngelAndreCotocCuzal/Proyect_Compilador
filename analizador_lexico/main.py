from PyQt5.QtWidgets import QApplication
from main_view import MainView
import sys


# compile_code()

app = QApplication(sys.argv)
main_view = MainView()

sys.exit(app.exec_())
