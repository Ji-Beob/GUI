from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView
from PyQt5.QtCore import *

# 심볼 테이블뷰 생성
class TableSymbolView(QTableWidget):
    def __init__(self, data, model, boxview):
        super().__init__()
        
        self.check_model = model
        self.box_view = boxview
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.setStyleSheet("selection-background-color : #8b00ff;" "selection-color : black;")

        # 이벤트 발생 시 연결
        self.cellClicked.connect(self.cell_click)
        
        self.tableSetting(data)
        
    
    def tableSetting(self, symbol_data):
        self.data = symbol_data
        # 테이블의 행과 열 크기 설정
        self.setRowCount(len(symbol_data))
        if len(symbol_data) != 0:
            self.setColumnCount(len(symbol_data[0])+1)
        
            header_labels = ["ID", "Type", "class", "xmin", "ymin", "xmax", "ymax", "orientation", "flip", "etc"]
            self.setHorizontalHeaderLabels(header_labels)

            number = 0
            for i, row in enumerate(symbol_data):
                for j, item in enumerate(row):
                    if j == 0:
                        number+=1
                        self.setItem(i, j, QTableWidgetItem(str(number)))
                        self.setItem(i, j+1, QTableWidgetItem(str(item)))
                    else:
                        self.setItem(i, j+1, QTableWidgetItem(str(item)))
        else:
            pass

    def setSignal(self, on_data_changed_from_view, get_data_func, notify_selected_index):
        self.on_data_changed_from_view = on_data_changed_from_view
        self.get_data = get_data_func
        self.on_selected = notify_selected_index


    def cell_click(self):
        self.clicked_row_index = (self.selectedIndexes())[0].row()
        # self.current_row = self.getTableCell(self.clicked_row_index)

        origin_index = self.returnOriginDataIndex(self.clicked_row_index)

        self.on_selected(origin_index)
        self.box_view.Clicked_rowdata_add(self.clicked_row_index)
        

    def getTableCell(self, i, j=None):
        result = []
        if j is None:
            for col in range(0, self.columnCount()):
                result.append(self.item(i, col).text())
        else:
            result.append(self.item(i, j).text())
        self.check_model.check = 1
        return result


    def returnOriginDataIndex(self, sorted_index):
        current_row = self.getTableCell(sorted_index).copy()
        for i in range(3, 8):
            current_row[i] = int(current_row[i])
        origin_index = self.data.index(current_row[1:10])

        return origin_index
    

    def selectionChange(self, i):  # ViewModel에서 사용
        self.setCurrentCell(i, 1)


# 라인 테이블뷰 생성
class TableLineView(QTableWidget):
    def __init__(self, line_data, arrow_data, model, lineview, arrow_view):
        super().__init__()

        self.check_model = model
        self.arrow_data = arrow_data
        self.tableSetting(line_data, arrow_data)

        # 추가 arrow table
        self.line_view = lineview
        self.arrow_view = arrow_view
        
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.setStyleSheet("selection-background-color : #8b00ff;" "selection-color : black;")

        # 이벤트 발생 시 연결
        self.cellClicked.connect(self.cell_click)
        
    
    def tableSetting(self, line_data, arrow_data):
        number = 0
        self.data = line_data
        # 테이블의 행과 열 크기 설정
        if len(line_data) != 0:
            self.setRowCount(len(line_data))
            self.setColumnCount(len(line_data[0])+2)
            
            header_labels = ["ID", "class", "xstart", "ystart", "xend", "yend", "arrow type", "arrow degree", "arrow location", "arrow count"]
            self.setHorizontalHeaderLabels(header_labels)
            for i, row in enumerate(line_data):
                for j, item in enumerate(row):
                    if j == 0:
                        number+=1
                        self.setItem(i, j, QTableWidgetItem(str(number)))
                        self.setItem(i, j+1, QTableWidgetItem(str(item)))
                    else:
                        self.setItem(i, j+1, QTableWidgetItem(str(item)))
                if len(arrow_data[i]) == 1:
                    if row[7] == 'None':
                        self.setItem(i, 9, QTableWidgetItem('0'))
                    else:
                        self.setItem(i, 9, QTableWidgetItem('1'))
                else:
                    self.setItem(i, 9, QTableWidgetItem(str(len(self.arrow_data[i]))))

    
    def setSignalLine(self, on_data_changed_from_view, get_data_func, notify_selected_index):
        self.on_data_changed_from_view = on_data_changed_from_view
        self.get_data = get_data_func
        self.on_selected = notify_selected_index


    def cell_click(self):
        self.clicked_row_index = (self.selectedIndexes())[0].row()
        # self.current_row = self.getTableCell(self.clicked_row_index)
        origin_index = self.returnOriginDataIndex(self.clicked_row_index)

        self.on_selected(origin_index)

        self.line_view.Clicked_rowdata_add(self.clicked_row_index)
        self.arrow_view.Clicked_rowdata_add(self.clicked_row_index)


    def getTableCell(self, i, j=None):
        result = []
        if j is None:
            for col in range(0, self.columnCount()-1):
                result.append(self.item(i, col).text())
        else:
            result.append(self.item(i, j).text())
        self.check_model.check = 0
        return result


    def returnOriginDataIndex(self, sorted_index):
        current_row = self.getTableCell(sorted_index).copy()
        for i in range(2, 6):
            current_row[i] = int(current_row[i])

        origin_index = self.data.index(current_row[1:9])
        return origin_index
    

    def selectionChangeLine(self, i):  # ViewModel에서 사용
        self.setCurrentCell(i, 0)
    

class TableView_Indetail(QTableWidget):
    def __init__(self, boxdata):
        super().__init__()

        self.box_data = boxdata
        self.setRowCount(0)
        
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.setStyleSheet("selection-background-color : #8b00ff;" "selection-color : black;")
    

    def Clicked_rowdata_add(self, row_num):
        # 테이블의 행과 열 크기 설정
        self.setRowCount(9)
        self.setColumnCount(1)
        
        header_labels = ["Type", "class", "xmin", "ymin", "xmax", "ymax", "orientation", "flip", "etc"]
        self.setVerticalHeaderLabels(header_labels)
        for i, row in enumerate(self.box_data[row_num]):
            for j, item in enumerate([row]):
                self.setItem(j, i, QTableWidgetItem(str(item)))


class TableView_Indetail_Line(QTableWidget):
    def __init__(self, linedata):
        super().__init__()

        self.line_data = linedata
        self.setRowCount(0)
        
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.setStyleSheet("selection-background-color : #8b00ff;" "selection-color : black;")
    

    def Clicked_rowdata_add(self, row_num):
        # 테이블의 행과 열 크기 설정
        self.setRowCount(5)
        self.setColumnCount(1)
        
        header_labels = ["class", "xstart", "ystart", "xend", "yend"]
        colheader_labels = ["line information"]
        self.setVerticalHeaderLabels(header_labels)
        self.setHorizontalHeaderLabels(colheader_labels)
        for i, row in enumerate(self.line_data[row_num]):
            for j, item in enumerate([row]):
                self.setItem(j, i, QTableWidgetItem(str(item)))
        
        self.setColumnWidth(0, 200)


# 화살표 추가 뷰 테이블뷰 생성
class TableArrowView(QTableWidget):
    def __init__(self, arrow_data):
        super().__init__()

        self.arrow_data = arrow_data
        self.setRowCount(0)
        
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.setStyleSheet("selection-background-color : #8b00ff;" "selection-color : black;")
    

    def Clicked_rowdata_add(self, row_num):
        # 테이블의 행과 열 크기 설정
        self.setRowCount(3)
        self.setColumnCount(len(self.arrow_data[row_num]))
        
        header_labels = ["arrow type", "arrow degree", "arrow location"]
        colheader_labels = ["arrow information"]
        self.setVerticalHeaderLabels(header_labels)
        self.setHorizontalHeaderLabels(colheader_labels)
        for i, row in enumerate(self.arrow_data[row_num]):
            for j, item in enumerate(row):
                self.setItem(j, i, QTableWidgetItem(str(item)))
        
        self.setColumnWidth(0, 150)


# -------------------------------------data_model과 view간의 상호작용 처리--------------------------------------------
class TableViewModel:
    def __init__(self, data_model, view, symbolview):
        super().__init__()

        # 모델 객체
        self.model = data_model
        self.selectedIndex = None
        self.symbol_view = symbolview

        # tableview 즉, TableWidget을 View객체로 지정
        self.tableView = view
        self.tableView.setSignal(on_data_changed_from_view=self.getChagedDataFromView, get_data_func=self.getBoxData,
                                 notify_selected_index=self.notify_selected_index)
        self.model.setTableSignal(notify_selected_to_table=self.get_selected_index)


    def getChagedDataFromView(self, row, value):
        self.updateBoxData(row, value)


    def getBoxData(self):
        return self.model.getBoxData()


    def updateBoxData(self, i, newData):
        self.model.setBoxData(i, newData)


    def get_selected_index(self, i):
        self.selectedIndex = i
        self.tableView.selectionChange(self.selectedIndex)
        self.symbol_view.Clicked_rowdata_add(self.selectedIndex)


    def notify_selected_index(self, i):
        self.model.setSelectedDataIndex(i, 1)
        self.model.check = 1


class TableViewModelLine:
    def __init__(self, data_model, view, lineview, arrowview):
        super().__init__()

        # 모델 객체
        self.model = data_model
        self.selectedIndex = None
        self.line_view = lineview
        self.arrow_view = arrowview

        # tableview 즉, TableWidget을 View객체로 지정
        self.tableView = view
        self.tableView.setSignalLine(on_data_changed_from_view=self.getChagedDataFromViewLine, get_data_func=self.getLineData,
                                 notify_selected_index=self.notify_selected_index_Line)
        self.model.setTableSignalLine(notify_selected_to_table=self.get_selected_index_Line)


    def getChagedDataFromViewLine(self, row, value):
        self.updateLineData(row, value)


    def getLineData(self):
        return self.model.getLineData()


    def updateLineData(self, i, newData):
        self.model.setLineData(i, newData)


    def get_selected_index_Line(self, i):
        self.selectedIndex = i
        self.tableView.selectionChangeLine(self.selectedIndex)
        self.line_view.Clicked_rowdata_add(self.selectedIndex)
        self.arrow_view.Clicked_rowdata_add(self.selectedIndex)


    def notify_selected_index_Line(self, i):
        self.model.setSelectedDataIndexLine(i, 1)