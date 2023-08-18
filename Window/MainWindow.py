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

        self.toolbar = self.addToolBar('오류 수정')
        self.toolbar.addAction(self.error_correction)


    def Create_Action(self):
        self.action_open_file = QAction(QIcon('./icon_img/xml.png'), 'img&xml', self)
        self.action_open_file.triggered.connect(self.openFileDialog)

        self.error_correction = QAction(QIcon('./icon_img/fixerror.png'), 'fix error', self)
        self.error_correction.triggered.connect(self.errorCorrectDialog)


    def openFileDialog(self):
        self.input_dialog = QDialog()

        # QDialog 세팅
        self.input_dialog.setWindowTitle('Input file')
        self.input_dialog.setWindowModality(2)                                       # Qt.ApplicationModal
        self.input_dialog.setGeometry(300, 100, 600, 300)
        self.input_dialog.setFixedSize(600, 300)

        self.input_dialog.imglabel = QLabel('도면 입력', self.input_dialog)
        self.input_dialog.imglabel.move(20, 10)
        self.input_dialog.xmllabel = QLabel('XML 입력', self.input_dialog)
        self.input_dialog.xmllabel.move(20, 35)
        self.input_dialog.corxmllabel = QLabel('정답XML 입력', self.input_dialog)
        self.input_dialog.corxmllabel.move(20, 60)

        self.input_dialog.img_btn = QPushButton('...', self.input_dialog)
        self.input_dialog.img_btn.resize(33, 22)
        self.input_dialog.img_btn.move(523,9)
        self.input_dialog.img_btn.clicked.connect(self.ImgBtnClick)

        self.input_dialog.xml_btn = QPushButton('...', self.input_dialog)
        self.input_dialog.xml_btn.resize(33, 22)
        self.input_dialog.xml_btn.move(523, 34)
        self.input_dialog.xml_btn.clicked.connect(self.XmlBtnClick)

        self.input_dialog.corxml_btn = QPushButton('...', self.input_dialog)
        self.input_dialog.corxml_btn.resize(33, 22)
        self.input_dialog.corxml_btn.move(523, 59)
        self.input_dialog.corxml_btn.clicked.connect(self.correctXmlBtnClick)

        '''File Path'''
        self.input_dialog.imgsource = QLineEdit(self.input_dialog)
        self.input_dialog.imgsource.resize(300, 20)
        self.input_dialog.imgsource.move(225, 10)
        self.input_dialog.imgsource.setReadOnly(True)
        self.input_dialog.imgsource.setPlaceholderText('도면 파일 경로')

        self.input_dialog.xmlsource = QLineEdit(self.input_dialog)
        self.input_dialog.xmlsource.resize(300, 20)
        self.input_dialog.xmlsource.move(225, 35)
        self.input_dialog.xmlsource.setReadOnly(True)
        self.input_dialog.xmlsource.setPlaceholderText('XML 파일 경로')

        self.input_dialog.corxmlsource = QLineEdit(self.input_dialog)
        self.input_dialog.corxmlsource.resize(300, 20)
        self.input_dialog.corxmlsource.move(225, 60)
        self.input_dialog.corxmlsource.setReadOnly(True)
        self.input_dialog.corxmlsource.setPlaceholderText('정답XML 파일 경로')

        self.input_dialog.path = QTextEdit(self.input_dialog)
        self.input_dialog.path.resize(550, 180)
        self.input_dialog.path.move(20, 85)
        self.input_dialog.path.append('File Path')

        '''Confirm button'''
        self.input_dialog.confirm = QPushButton('OK', self.input_dialog)
        self.input_dialog.confirm.move(480, 250)
        self.input_dialog.confirm.clicked.connect(self.FileOkBtnClick)

        self.input_dialog.show()


    def errorCorrectDialog(self):
        self.error_correct_dialog = QDialog()

        # QDialog 세팅
        self.error_correct_dialog.setWindowTitle('Error Verification')
        self.error_correct_dialog.setWindowModality(2)
        self.error_correct_dialog.setGeometry(300, 100, 600, 300)
        self.error_correct_dialog.setFixedSize(250, 50)
        
        # QDialog 내부 위젯 정리
        layout_ = QHBoxLayout()
        object_ID_Label = QLabel('객체 ID 입력')
        object_ID = QLineEdit()
        object_ID.setValidator(QIntValidator())     # 숫자만 입력받도록 설정
        click_button = QPushButton('오류 수정')

        layout_.addWidget(object_ID_Label)
        layout_.addWidget(object_ID)
        layout_.addWidget(click_button)

        self.error_correct_dialog.setLayout(layout_)

        self.error_correct_dialog.show()


    def ImgBtnClick(self):
        self.imgfilepath = QFileDialog.getOpenFileName(self, '열기', './', filter='*.jpg *.jpeg *.png')
        self.input_dialog.imgsource.setText(self.imgfilepath[0])
        self.input_dialog.path.append(self.imgfilepath[0])


    def XmlBtnClick(self):
        self.xmlfilepath = QFileDialog.getOpenFileName(self, '열기', './', filter='*.xml')
        self.input_dialog.xmlsource.setText(self.xmlfilepath[0])
        self.input_dialog.path.append(self.xmlfilepath[0])


    def correctXmlBtnClick(self):
        self.corxmlfilepath = QFileDialog.getOpenFileName(self, '열기', './', filter='*.xml')
        self.input_dialog.corxmlsource.setText(self.corxmlfilepath[0])
        self.input_dialog.path.append(self.corxmlfilepath[0])


    def FileOkBtnClick(self):
        self.input_dialog.close()
        self.callMappedArea(img_path=self.imgfilepath[0], xml_path=self.xmlfilepath[0], corxml_path=self.corxmlfilepath[0])

    
    def callMappedArea(self, img_path, xml_path, corxml_path):
        self.subwindow = MappedWindow(img=img_path, xml=xml_path, cor=corxml_path)
        self.showResult()


    def showResult(self):
        self.error_TabView = QTabWidget()
        self.setCentralWidget(self.error_TabView)
        self.xml_Symbol = ParseXML_Symbol(self.xmlfilepath[0])
        self.corxml_Symbol = ParseXML_Symbol(self.corxmlfilepath[0])


        # tab UI
        self.createErrorTabUiSym()
        self.createErrorTabUiLine()
        self.error_TabView.addTab(self.sym_scroll_area, 'symbol&text result image')
        self.error_TabView.addTab(self.line_scroll_area, 'line result image')

    
    def createErrorTabUiSym(self):
        self.sym_scroll_area = QScrollArea(self)
        self.sym_scroll_area.setWidgetResizable(True)
        self.sym_scroll_area.setGeometry(0, 0, 600, 700)
        self.sym_scroll_area.setStyleSheet("background-color: rgb(179, 177, 178) ")

        self.widget_ = QWidget(self.sym_scroll_area)
        self.symbol_layout = QVBoxLayout()

        image = QImage(self.imgfilepath[0])
        font = QFont("Arial", 11)

        for i in range(0, len(self.xml_Symbol)):
            sym_list = self.xml_Symbol[i]
            corsym_list = self.corxml_Symbol[i]

            width = sym_list[4] - sym_list[2]
            height = sym_list[5] - sym_list[3]

            # 객체 1개의 결과를 담을 위젯과 레이아웃
            widget_ = QWidget(self.widget_)
            layout_ = QHBoxLayout()
            widget_.setStyleSheet("background-color: rgb(255, 255, 255) ")
            
            # 객체 ID
            object_ID = QLabel('ID: {0}'.format(i+1))
            object_ID.setFixedWidth(50)
            object_ID.setStyleSheet("border: none")
            object_ID.setFont(font)
            object_ID.setAlignment(Qt.AlignCenter)  
            layout_.addWidget(object_ID)
            
            # 객체 type
            object_type = QLabel(sym_list[0])
            object_type.setFixedWidth(150)
            object_type.setStyleSheet("border: none")
            object_type.setFont(font)
            object_type.setAlignment(Qt.AlignCenter) 
            layout_.addWidget(object_type)

            ### 검증 도면 이미지
            object_img = QLabel()

            # orientation에 따라서 회전변환
            sym_box = QRect(sym_list[2], sym_list[3], width, height)
            center = sym_box.center()

            # 회전 변환 행렬 생성
            transform = QTransform()
            transform.translate(center.x(), center.y())
            transform.rotate(-sym_list[6])
            transform.translate(-center.x(), -center.y())
            sym_box = transform.mapRect(sym_box)

            # 이미지 객체 생성
            sym_img = QPixmap.fromImage(image.copy(sym_box))
            transform_pix = QTransform()
            transform_pix.translate(center.x(), center.y())
            transform_pix.rotate(sym_list[6])
            transform_pix.translate(-center.x(), -center.y())
            sym_img = sym_img.transformed(transform_pix, mode=Qt.SmoothTransformation)

            # 이미지 객체 표시
            if width > 500:
                height = 500/width*height
                width = 500
                sym_img = sym_img.scaled(width, height)
            object_img.setPixmap(sym_img)
            object_img.setFixedSize(500, height)
            object_img.setStyleSheet("border: none")
            object_img.setAlignment(Qt.AlignCenter)
            layout_.addWidget(object_img)

            ### 정답 도면 이미지
            corobject_img = QLabel()

            corobject_type = QLabel(corsym_list[0])
            corobject_type.setFixedWidth(150)
            corobject_type.setStyleSheet("border: none")
            corobject_type.setFont(font)
            corobject_type.setAlignment(Qt.AlignCenter)       
            layout_.addWidget(corobject_type)

            corwidth = corsym_list[4] - corsym_list[2]
            corheight = corsym_list[5] - corsym_list[3]

            # orientation에 따라서 회전변환
            corsym_box = QRect(corsym_list[2], corsym_list[3], corwidth, corheight)
            center = corsym_box.center()

            # 회전 변환 행렬 생성
            transform = QTransform()
            transform.translate(center.x(), center.y())
            transform.rotate(-corsym_list[6])
            transform.translate(-center.x(), -center.y())
            corsym_box = transform.mapRect(corsym_box)

            # 이미지 객체 생성
            corsym_img = QPixmap.fromImage(image.copy(corsym_box))
            transform_pix = QTransform()
            transform_pix.translate(center.x(), center.y())
            transform_pix.rotate(corsym_list[6])
            transform_pix.translate(-center.x(), -center.y())
            corsym_img = corsym_img.transformed(transform_pix, mode=Qt.SmoothTransformation)
            corobject_img.setAlignment(Qt.AlignCenter)

            # 이미지 객체 표시
            if corwidth > 500:
                corheight = 500/width*height
                corwidth = 500
                corsym_img = corsym_img.scaled(corwidth, corheight)
            corobject_img.setPixmap(corsym_img)
            corobject_img.setFixedSize(500, corheight)
            corobject_img.setStyleSheet("border: none")
            layout_.addWidget(corobject_img)

            # 위젯 설정
            widget_.setLayout(layout_)
            widget_.setFixedWidth(1550)
            self.symbol_layout.addWidget(widget_)
        
        self.widget_.setLayout(self.symbol_layout)
        self.sym_scroll_area.setWidget(self.widget_)

    def createErrorTabUiLine(self):
        self.line_scroll_area = QScrollArea(self)
        self.line_scroll_area.setWidgetResizable(True)
        self.line_scroll_area.setGeometry(0, 0, 600, 700)
        self.line_scroll_area.setStyleSheet("background-color: rgb(179, 177, 178) ")