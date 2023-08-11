import sys
from PyQt5.QtWidgets import QApplication

from Window.MainWindow import *


if __name__ == '__main__':
    # QApplication 인스턴스 생성
    app = QApplication(sys.argv)

    # 창 인스턴스 생성
    mainWindow = MainWindow()

    # 창 표시
    mainWindow.show()

    # 이벤트 루프 실행
    sys.exit(app.exec_())