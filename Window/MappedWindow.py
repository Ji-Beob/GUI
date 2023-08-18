import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from Utils.Xml_load import *
from Utils.DataModel import *
from View.TableView import *
from View.SceneView import *


class MappedWindow(QMainWindow):
    def __init__(self, img, xml, cor):
        super().__init__()
        self.title = img
        self.img_name = os.path.basename(img).split('/')[-1]
        self.img_path = img
        self.xml_path = xml
        self.corxml_path = cor

        # xml 데이터 받아옴
        self.xml_Symbol = ParseXML_Symbol(self.xml_path)
        self.xml_Line, self.xml_Arrow = ParseXML_Line(self.xml_path)

        self.corxml_Symbol = ParseXML_Symbol(self.corxml_path)
        self.corxml_Line, self.corxml_Arrow = ParseXML_Line(self.corxml_path)

        # 도면 내 객체 정의(심볼/텍스트/라인/애로우)
        self.Symbol_model = SymbolModel(self.xml_Symbol)
        self.Line_model = LineModel(self.xml_Line, self.xml_Arrow)

        # window UI 설정
        self.Initwindowui(title=self.title)

        # 툴바 생성
        self.create_Action()
        self.create_ToolBar()

    # 색 입력 받을 툴바 생성
    def create_ToolBar(self):
        self.toolbar = self.addToolBar('toolbar')
        self.toolbar.addAction(self.color_change)


    def create_Action(self):
        self.color_change = QAction(QIcon('./icon_img/colorChange.png'), 'color change', self)
        self.color_change.triggered.connect(self.openColorDialog)


 #----------------------------------------------------------------------기능 구현 중------------------------------------------------------------------       

    def openColorDialog(self):
        self.color_dialog = QDialog()

        # QDialog 세팅
        self.color_dialog.setWindowTitle('color change')
        self.color_dialog.setWindowModality(2)
        self.color_dialog.setGeometry(300, 100, 500, 200)
        self.color_dialog.setFixedSize(300, 150)

        # RGB 값 입력 받기
        self.color_dialog.layout_ = QHBoxLayout()
        self.color_dialog.combobox = QComboBox()
        self.color_dialog.combobox.addItems(["Symbol", "Text", "continuous_line", 'specbreaker_line', 'dimension_line', 'annotation_line', 'leader_line', 'short_dotted_line'])

        self.color_dialog.colorcodeR = QLabel('R')
        self.color_dialog.colorcodeG = QLabel('G')
        self.color_dialog.colorcodeB = QLabel('B')
        self.color_dialog.codeR = QLineEdit()
        self.color_dialog.codeG = QLineEdit()
        self.color_dialog.codeB = QLineEdit()

        self.color_dialog.layout_.widgetR = QWidget()
        self.color_dialog.layout_.widgetG = QWidget()
        self.color_dialog.layout_.widgetB = QWidget()
        self.color_dialog.layout_.widgetR.layout_ = QHBoxLayout()
        self.color_dialog.layout_.widgetG.layout_ = QHBoxLayout()
        self.color_dialog.layout_.widgetB.layout_ = QHBoxLayout()

        self.color_dialog.layout_.widgetR.layout_.addWidget(self.color_dialog.colorcodeR)
        self.color_dialog.layout_.widgetR.layout_.addWidget(self.color_dialog.codeR)
        self.color_dialog.layout_.widgetG.layout_.addWidget(self.color_dialog.colorcodeG)
        self.color_dialog.layout_.widgetG.layout_.addWidget(self.color_dialog.codeG)
        self.color_dialog.layout_.widgetB.layout_.addWidget(self.color_dialog.colorcodeB)
        self.color_dialog.layout_.widgetB.layout_.addWidget(self.color_dialog.codeB)

        self.color_dialog.layout_.widgetR.setLayout(self.color_dialog.layout_.widgetR.layout_)
        self.color_dialog.layout_.widgetG.setLayout(self.color_dialog.layout_.widgetG.layout_)
        self.color_dialog.layout_.widgetB.setLayout(self.color_dialog.layout_.widgetB.layout_)

        self.color_dialog.layout_.widget_ = QWidget()
        self.color_dialog.layout_.widget_.layout_ = QVBoxLayout()
        self.color_dialog.layout_.widget_.layout_.addWidget(self.color_dialog.layout_.widgetR)
        self.color_dialog.layout_.widget_.layout_.addWidget(self.color_dialog.layout_.widgetG)
        self.color_dialog.layout_.widget_.layout_.addWidget(self.color_dialog.layout_.widgetB)
        self.color_dialog.layout_.widget_.setLayout(self.color_dialog.layout_.widget_.layout_)

        self.color_dialog.button = QPushButton('color change')

        self.color_dialog.layout_.addWidget(self.color_dialog.combobox)
        self.color_dialog.layout_.addWidget(self.color_dialog.layout_.widget_)
        self.color_dialog.layout_.addWidget(self.color_dialog.button)

        self.color_dialog.setLayout(self.color_dialog.layout_)

        self.color_dialog.show()

#----------------------------------------------------------------------------------------------------------------------------------------

    def Initwindowui(self, title):
        self.setWindowTitle(title)
        self.move(100, 100)
        self.resize(1600, 800)

        # 도면 영역
        # window 화면 구성 (window > widget > widget_layout)
        self.sceneView = SceneView(self.img_path, self.Line_model)
        self.sceneViewModel = SceneViewModel(self.Symbol_model, self.Line_model, self.sceneView)
        self.setCentralWidget(self.sceneView)

        # 테이블 영역
        self.Tabview()
        self.Createdock() # self.tabview

        self.show()

# xml 테이블 도킹 위젯--------------------------------------------------------------------------------------------------
    def Createdock(self):
        # 도킹 위젯 세팅
        self.dockingWidget = QDockWidget("XML Result")
        self.setCorner(Qt.TopRightCorner, Qt.RightDockWidgetArea)               # 위젯의 오른쪽 위 모서리에 도크 위젯 배치
        self.dockingWidget.setMinimumSize(int(self.frameGeometry().width() * 0.25), self.frameGeometry().height())

        # 2개 위젯을 담을 빈 위젯
        self.emptyWidgetforLayout = QWidget()
        self.dockingWidget.setWidget(self.emptyWidgetforLayout)

        # 체크박스와 클릭버튼을 위한 위젯
        self.emptyWidgetforButton = QWidget()
        self.symbol_CheckBox = QCheckBox('Symbol', self)
        self.text_CheckBox = QCheckBox('Text', self)
        self.line_CheckBox = QCheckBox('Line', self)
        self.arrow_CheckBox = QCheckBox('Arrow', self)
        self.id_CheckBox = QCheckBox('ID', self)
        self.applyButton = QPushButton('click', self.emptyWidgetforButton)
        self.applyButton.clicked.connect(self.Checked_instance)
        self.symbol_CheckBox.setChecked(True)
        self.text_CheckBox.setChecked(True)
        self.line_CheckBox.setChecked(True)
        self.arrow_CheckBox.setChecked(True)
        self.id_CheckBox.setChecked(False)
        
        # 레이아웃에 버튼 위젯 배치
        self.layoutforButton = QHBoxLayout()
        self.layoutforButton.addWidget(self.symbol_CheckBox)
        self.layoutforButton.addWidget(self.text_CheckBox)
        self.layoutforButton.addWidget(self.line_CheckBox)
        self.layoutforButton.addWidget(self.arrow_CheckBox)
        self.layoutforButton.addWidget(self.id_CheckBox)
        self.layoutforButton.addWidget(self.applyButton)
        self.emptyWidgetforButton.setLayout(self.layoutforButton)
        
        # 도킹창 내부 레이아웃 설정
        self.layoutInDock = QVBoxLayout()
        self.layoutInDock.addWidget(self.emptyWidgetforButton)
        self.layoutInDock.addWidget(self.tabView)               # self.tabview from TabView method
        self.emptyWidgetforLayout.setLayout(self.layoutInDock)
        self.dockingWidget.setFloating(False)

        # Window에 도킹창 배치
        self.addDockWidget(Qt.RightDockWidgetArea, self.dockingWidget)


    def Tabview(self):
        # tab을 담을 위젯
        self.tabView = QWidget()
        self.tabView.tabLayout = QVBoxLayout()

        # tab 위젯
        self.tabView.tabs = QTabWidget()
        self.tabView.tab1 = QWidget()
        self.tabView.tab2 = QWidget()

        # tab UI
        self.Createtabui()
        self.tabView.tabs.addTab(self.tabView.tab1, 'Recognized Symbol')
        self.tabView.tabs.addTab(self.tabView.tab2, 'Recognized Line')
        self.tabView.tabLayout.addWidget(self.tabView.tabs)
        self.tabView.setLayout(self.tabView.tabLayout)


    # tab UI
    def Createtabui(self):
        # tab1 layout
        self.tabView.tab1.Layout = QVBoxLayout()
        self.tab1_Table = TableView_Indetail(self.xml_Symbol)
        self.tab2_Table = TableSymbolView(self.xml_Symbol, self.Symbol_model, self.tab1_Table)
        self.tableViewModel = TableViewModel(self.Symbol_model, self.tab2_Table, self.tab1_Table)
        self.tabView.tab1.Layout.addWidget(self.tab2_Table)
        self.tabView.tab1.Layout.addWidget(self.tab1_Table)
        self.tabView.tab1.setLayout(self.tabView.tab1.Layout)

        # tab2 layout
        self.tabView.tab2.Layout = QVBoxLayout()
        self.tabView.tab2.Layout.widget_ = QWidget()
        self.tabView.tab2.Layout.widget_.layout_ = QHBoxLayout()
        self.tab3_Table = TableView_Indetail_Line(self.xml_Line)
        self.tab4_Table = TableArrowView(self.xml_Arrow)
        self.tab5_Table = TableLineView(self.xml_Line, self.xml_Arrow, self.Symbol_model, self.tab3_Table, self.tab4_Table)
        self.tableViewModelLine = TableViewModelLine(self.Line_model, self.tab5_Table, self.tab3_Table, self.tab4_Table)
        self.tabView.tab2.Layout.widget_.layout_.addWidget(self.tab3_Table)
        self.tabView.tab2.Layout.widget_.layout_.addWidget(self.tab4_Table)
        self.tabView.tab2.Layout.widget_.setLayout(self.tabView.tab2.Layout.widget_.layout_)
        self.tabView.tab2.Layout.addWidget(self.tab5_Table)
        self.tabView.tab2.Layout.addWidget(self.tabView.tab2.Layout.widget_)
        self.tabView.tab2.setLayout(self.tabView.tab2.Layout)
#-------------------------------------------------------------------------------------------------------------------------

    # 체크박스 연결
    def Checked_instance(self):
        self.sceneView.Show_object(self.symbol_CheckBox.isChecked(), self.text_CheckBox.isChecked(),
                                 self.line_CheckBox.isChecked(), self.arrow_CheckBox.isChecked(), self.id_CheckBox.isChecked())
        
    
