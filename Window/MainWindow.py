# -*- coding: utf-8 -*-

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from Window.MappedWindow import *

class MainWindow(QMainWindow):                                  # QMainWindow를 상속받으면 클래스 인스턴스 생성 시 창이 됨
    def __init__(self):
        super().__init__()
        self.initMainUI()

    def initMainUI(self):                                       # 메인 window 설정
        self.setWindowTitle('도면 인식 결과 가시화 프로그램')
        self.move(300,100)
        self.resize(1000, 500)
        self.statusBar()                                        # 상태바 생성
        
        self.Create_Action()
        self.Create_MenuBar()                                          # 메뉴바 생성
        self.Create_ToolBar()                                          # 툴바 생성


    def Create_MenuBar(self):
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)                                 # Mac에서 사용
        menubar.addMenu('&File')
        menubar.addMenu('&view')
        menubar.addMenu('&tool')
        menubar.addMenu('&help')


    def Create_ToolBar(self):
        self.toolbar = self.addToolBar('start')
        self.toolbar.addAction(self.action_open_file)


    def Create_Action(self):
        self.action_open_file = QAction(QIcon('./icon_img/xml.png'), 'img&xml', self)
        self.action_open_file.triggered.connect(self.openfileDialog)


    def openfileDialog(self):
        self.dialog = QDialog()

        # QDialog 세팅
        self.dialog.setWindowTitle('Input file')
        self.dialog.setWindowModality(2)                                       # Qt.ApplicationModal
        self.dialog.setGeometry(300, 100, 600, 300)
        self.dialog.setFixedSize(600, 300)

        self.dialog.imglabel = QLabel('도면 입력', self.dialog)
        self.dialog.imglabel.move(20, 10)
        self.dialog.xmllabel = QLabel('XML 입력', self.dialog)
        self.dialog.xmllabel.move(20, 35)

        self.dialog.img_btn = QPushButton('...', self.dialog)
        self.dialog.img_btn.resize(33, 22)
        self.dialog.img_btn.move(523,9)
        self.dialog.img_btn.clicked.connect(self.ImgBtnClick)

        self.dialog.xml_btn = QPushButton('...', self.dialog)
        self.dialog.xml_btn.resize(33, 22)
        self.dialog.xml_btn.move(523, 34)
        self.dialog.xml_btn.clicked.connect(self.XmlBtnClick)

        '''File Path'''
        self.dialog.imgsource = QLineEdit(self.dialog)
        self.dialog.imgsource.resize(300, 20)
        self.dialog.imgsource.move(225, 10)
        self.dialog.imgsource.setReadOnly(True)
        self.dialog.imgsource.setPlaceholderText('도면 파일 경로')

        self.dialog.xmlsource = QLineEdit(self.dialog)
        self.dialog.xmlsource.resize(300, 20)
        self.dialog.xmlsource.move(225, 35)
        self.dialog.xmlsource.setReadOnly(True)
        self.dialog.xmlsource.setPlaceholderText('XML 파일 경로')

        self.dialog.path = QTextEdit(self.dialog)
        self.dialog.path.resize(550, 180)
        self.dialog.path.move(20, 60)
        self.dialog.path.append('File Path')

        '''Confirm button'''
        self.dialog.confirm = QPushButton('OK', self.dialog)
        self.dialog.confirm.move(480, 250)
        self.dialog.confirm.clicked.connect(self.FileOkBtnClick)

        self.dialog.show()

    def ImgBtnClick(self):
        self.imgfilepath = QFileDialog.getOpenFileName(self, '열기', './', filter='*.jpg *.jpeg *.png')
        self.dialog.imgsource.setText(self.imgfilepath[0])
        self.dialog.path.append(self.imgfilepath[0])

    def XmlBtnClick(self):
        self.xmlfilepath = QFileDialog.getOpenFileName(self, '열기', './', filter='*.xml')
        self.dialog.xmlsource.setText(self.xmlfilepath[0])
        self.dialog.path.append(self.xmlfilepath[0])

    def FileOkBtnClick(self):
        self.dialog.close()
        self.callMappedArea(img_path=self.imgfilepath[0], xml_path=self.xmlfilepath[0])
    
    def callMappedArea(self, img_path, xml_path):
        self.subwindow = MappedWindow(img=img_path, xml=xml_path)