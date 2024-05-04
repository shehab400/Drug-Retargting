# main.py

import sys
from PyQt5.QtWidgets import QApplication
from Gui import DrugRetargetingGUI
import qdarkstyle

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DrugRetargetingGUI()
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    window.show()
    sys.exit(app.exec_())
