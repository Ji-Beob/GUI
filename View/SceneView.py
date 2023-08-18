from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsItem, QGraphicsRectItem, QGraphicsLineItem, QGraphicsTextItem
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QColor
import math

# QGraphicsView: 그래픽 요소를 표시하는 창 역할
# QGraphicsScene: 그래픽 요소를 담는 컨테이너 역할
class SceneView(QGraphicsView):
    def __init__(self, backgroundimg, model):
        super().__init__()

        # 변수 설정
        self.currentItem = None
        self.line_Box = None
        self.zoomInCnt = 0
        self.zoomOutCnt = 0
        self.NOTHING_COLOR = QColor(0, 0, 0, 0)
        self.SELECTED_COLOR = QColor(95, 0, 255, 170)
        self.bndboxList = []
        self.lineList = []
        self.arrowList = []
        self.idList = []
        self.model = model  # 라인 모델, Arrow data 가져오는 용도로 사용됨

        # View 객체에 scene 요소들 넣기
        self.symbol_line_scene = GraphicsScene(self.bndboxList, self.lineList, self.arrowList)
        self.symbol_line_scene.Set_image(backgroundimg)
        self.setScene(self.symbol_line_scene)

        # 도면 설정
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
              
        # 요소 색상 변화
        self.symbol_line_scene.changeSelectedItemColor = self.Changeselcteditemcolor
        self.symbol_line_scene.changeSelectedItemColorLine = self.Changeselcteditemcolorline


    # 박스 데이터 받아오는 메서드
    def Setsignal(self, get_data_func, notify_selected_index, get_data_func_line):
        self.get_data_line = get_data_func_line
        self.get_data = get_data_func
        self.symbol_line_scene.on_selected = notify_selected_index      # 도면 -> 테이블 / 테이블 -> 도면 결정

    
    # 박스 데이터 초기화
    def Setinitdata(self):
        self.data = self.get_data()
        data_num = len(self.data)
        for index in range(data_num):
            box = BoundingBox(index)
            if self.data[index][0] == 'text':
                box.type = 0
                pen = QPen(Qt.red)
                pen.setWidth(3)
                box.setPen(pen)
            else:
                box.type = 1
                pen = QPen(Qt.green)
                pen.setWidth(3)
                box.setPen(pen)

            box.setFlag(QGraphicsItem.ItemIsSelectable, False)
            box.setFlag(QGraphicsItem.ItemIsMovable, False)
            self.symbol_line_scene.addItem(box)
            xmin = int(self.data[index][2])
            ymin = int(self.data[index][3])
            width = int(self.data[index][4]) - xmin
            height = int(self.data[index][5]) - ymin
            rect = QRectF(xmin, ymin, width, height)
            box.setRect(rect)
            if int(self.data[index][6]) != 0:
                center = rect.center()

                # 회전 변환 행렬 생성
                transform = QTransform()
                transform.translate(center.x(), center.y())
                transform.rotate(-self.data[index][6])
                transform.translate(-center.x(), -center.y())
                box.setTransform(transform)
                          
            self.bndboxList.append(box)
            

    # 라인 데이터 초기화
    def Setinitdataline(self):
        self.line_data = self.get_data_line()
        data_num = len(self.line_data)
        for index in range(data_num):
            line = BoundingLine(index)
            line.setFlag(QGraphicsItem.ItemIsSelectable, False)
            line.setFlag(QGraphicsItem.ItemIsMovable, False)
            self.symbol_line_scene.addItem(line)
            self.xstart = int(self.line_data[index][1])
            self.ystart = int(self.line_data[index][2])
            self.xend = int(self.line_data[index][3])
            self.yend = int(self.line_data[index][4])
            line_length = ((self.xend-self.xstart)**2+(self.yend-self.ystart)**2)**0.5
            l = QLineF(self.xstart, self.ystart, self.xend, self.yend)
            if (self.line_data[index][0]=='continuous_thick_line') or (self.line_data[index][0]=='continuous_line'):
                line.setLine(l)
                pen = QPen(QColor(92, 209, 229, 150))
                pen.setWidth(10)
                line.setPen(pen)
            elif self.line_data[index][0]=='specbreaker_line':
                line.setLine(l)
                pen = QPen(QColor(0, 0, 255, 150))
                pen.setWidth(10)
                line.setPen(pen)
            elif (self.line_data[index][0]=='dimension_line') or (self.line_data[index][0]=='extension_line'):
                line.setLine(l)
                pen = QPen(QColor(255, 255, 54, 150))
                pen.setWidth(10)
                line.setPen(pen)
            elif self.line_data[index][0]=='annotation_line':
                line.setLine(l)
                pen = QPen(QColor(255, 108, 235, 150))
                pen.setWidth(10)
                line.setPen(pen)
            elif self.line_data[index][0]=='leader_line':
                line.setLine(l)
                pen = QPen(QColor(29, 219, 22, 150))
                pen.setWidth(10)
                line.setPen(pen)
            elif self.line_data[index][0]=='short_dotted_line':
                line.setLine(l)
                pen = QPen(QColor(153, 0, 76, 150))
                pen.setWidth(10)
                line.setPen(pen)
            else:
                line.setLine(l)
                pen = QPen(QColor(237, 0, 203, 150))
                pen.setWidth(10)
                line.setPen(pen)
            
            self.lineList.append(line)
        
        
            # arrow
            arrow_data = self.model.arrow_data[index]
            # box 제작
            arrowlist = []
            for idx in range(0,len(arrow_data)):
                box = BoundingBox(type = 3)
                box.setFlag(QGraphicsItem.ItemIsSelectable, False)
                box.setFlag(QGraphicsItem.ItemIsMovable, False)

                pen = QPen(QColor(255, 130, 36))
                pen.setWidth(3)
                box.setPen(pen)                
                if arrow_data[idx][0] == 'flow_arrow':
                    rect, transform = self.Arrow_rect(24, 36, arrow_data, self.line_data, line_length, idx, index)
                    box.setRect(rect)
                    box.setTransform(transform)
                elif arrow_data[idx][0] == 'sharp_arrow':
                    rect, transform  = self.Arrow_rect(20, 30, arrow_data, self.line_data, line_length, idx, index)
                    box.setRect(rect)
                    box.setTransform(transform)
                elif arrow_data[idx][0] == 'signal_arrow':
                    rect, transform  = self.Arrow_rect(20, 30, arrow_data, self.line_data, line_length, idx, index)
                    box.setRect(rect)
                    box.setTransform(transform)
                elif arrow_data[idx][0] == 'break':
                    arrow_width = 50     # 화살표 폭
                    arrow_height = 20   # 화살표 높이
                    degree = float(arrow_data[idx][1])
                    location = float(arrow_data[idx][2])
                    if self.line_data[index][1]-self.line_data[index][3] == 0:
                        xmin = float(self.line_data[index][1]) - float(arrow_width/2)
                        ymin = float(self.line_data[index][2]) + float(line_length*location) - float(arrow_height/2)
                        rect = QRectF(xmin, ymin, arrow_width, arrow_height)
                        box.setRect(rect)
                    elif self.line_data[index][2]-self.line_data[index][4] == 0:
                        xmin = float(self.line_data[index][1]) + float(line_length*location) - float(arrow_height/2)
                        ymin = float(self.line_data[index][4]) - arrow_width/2
                        rect = QRectF(xmin, ymin, arrow_height, arrow_width)
                        box.setRect(rect)
                    else:
                        xmin = float(self.line_data[index][1]) + float(line_length*location) - float(arrow_height/2)
                        ymin = float(self.line_data[index][4]) - arrow_width/2
                        rect = QRectF(xmin, ymin, arrow_height, arrow_width)

                        center = rect.center()
                        # 회전 변환 행렬 생성
                        transform = QTransform()
                        if degree == 0:
                            theta = math.atan((self.yend-self.ystart)/(self.xend-self.xstart))
                            theta = math.degrees(theta)
                            transform.translate(center.x() - arrow_height/2, center.y())
                            transform.rotate(theta)
                            transform.translate(-center.x() + arrow_height/2, -center.y())
                        elif degree == 1:
                            theta = math.atan((self.xend-self.xstart)/(self.yend-self.ystart))
                            theta = math.degrees(theta)
                            transform.translate(center.x() + arrow_height/2, center.y())
                            transform.rotate(theta)
                            transform.translate(-center.x() - arrow_height/2, -center.y())
                        # 사각형 좌표 회전
                        box.setRect(rect)
                        box.setTransform(transform)
                else:
                    rect=QRectF(0,0,0,0)
                    box.setRect(rect)

                arrowlist.append(box)
                self.symbol_line_scene.addItem(box)
            self.arrowList.append(arrowlist)


    def Arrow_rect(self, width, height, arrow_data, line_data, line_length, idx, index):
        arrow_width = width     # 화살표 폭
        arrow_height = height   # 화살표 높이
        degree = float(arrow_data[idx][1])
        location = float(arrow_data[idx][2])
        transform = QTransform()
        if line_data[index][1]-line_data[index][3] == 0:                                # 수직
            if degree == 0:                     # degree 0 (시작점을 바라봄)
                xmin = float(line_data[index][1]) - float(arrow_width/2) 
                ymin = float(line_data[index][2]) + float(line_length*location)
            elif degree == 1:                   # degree 1 (끝점을 바라봄)
                xmin = float(line_data[index][1]) - float(arrow_width/2)
                ymin = float(line_data[index][4]) - float(line_length*(1-location)) - float(arrow_height)
            rect = QRectF(xmin, ymin, arrow_width, arrow_height)
        elif line_data[index][2]-line_data[index][4] == 0:                              # 수평
            if degree == 0:                     # degree 0 (시작점을 바라봄)
                xmin = float(line_data[index][1]) + float(line_length*location)
                ymin = float(line_data[index][2]) - float(arrow_width/2)
            elif degree == 1:                   # degree 1 (끝점을 바라봄)
                xmin = float(line_data[index][3]) - float(arrow_height) - float(line_length*(1-location))
                ymin = float(line_data[index][2]) - float(arrow_width/2)
            rect = QRectF(xmin, ymin, arrow_height, arrow_width)
        else:
            if degree == 0:                     # degree 0 (시작점을 바라봄)
                xmin = float(line_data[index][1]) + float(line_length*location)
                ymin = float(line_data[index][2]) - float(arrow_width/2)
            elif degree == 1:                   # degree 1 (끝점을 바라봄)
                xmin = float(line_data[index][3]) - float(arrow_height) - float(line_length*(1-location))
                ymin = float(line_data[index][4]) - float(arrow_width/2)
            rect = QRectF(xmin, ymin, arrow_height, arrow_width)

            center = rect.center()
            # 회전 변환 행렬 생성
            if degree == 0:
                theta = math.atan((self.yend-self.ystart)/(self.xend-self.xstart))
                theta = math.degrees(theta)
                transform.translate(center.x() - arrow_height/2, center.y())
                transform.rotate(theta)
                transform.translate(-center.x() + arrow_height/2, -center.y())
            elif degree:
                theta = math.atan((self.yend-self.ystart)/(self.xend-self.xstart))
                theta = math.degrees(theta)
                transform.translate(center.x() + arrow_height/2, center.y())
                transform.rotate(theta)
                transform.translate(-center.x() - arrow_height/2, -center.y())
        return rect, transform


    # 아이디 바운딩 박스 만들고 객체에 표시
    def Id_rect(self):
        for id, box in enumerate(self.bndboxList):
            object = QGraphicsTextItem()
            object.type = 4
            object.setFlag(QGraphicsItem.ItemIsSelectable, False)
            object.setFlag(QGraphicsItem.ItemIsMovable, False)
            object.setPlainText('{0}'.format(id+1))
            object.setDefaultTextColor(QColor(Qt.transparent))
            font = QFont()
            font.setBold(True)
            object.setFont(font)

            rect = box.rect()
            object.setPos(rect.bottomLeft())
            self.symbol_line_scene.addItem(object)
            self.idList.append(object)
        
        for id, line in enumerate(self.lineList):
            object = QGraphicsTextItem()
            object.type = 5
            object.setFlag(QGraphicsItem.ItemIsSelectable, False)
            object.setFlag(QGraphicsItem.ItemIsMovable, False)
            object.setPlainText('{0}'.format(id+1))
            object.setDefaultTextColor(QColor(Qt.transparent))
            font = QFont()
            font.setBold(True)
            object.setFont(font)

            x = line.boundingRect().left()
            y = line.boundingRect().bottom()
            object.setPos(x,y)
            self.symbol_line_scene.addItem(object)
            self.idList.append(object)


    def Selectionchange(self, idx):                                 # ViewModel
        current_item = self.bndboxList[idx]
        self.centerOn(current_item)                                 # 중앙에 보이도록 정렬
        self.Changeselcteditemcolor(current_item)


    def Selectionchangeline(self, idx):                             # ViewModel
        current_item = self.lineList[idx]
        self.centerOn(current_item)                                 # 중앙에 보이도록 정렬
        self.Changeselcteditemcolorline(current_item)


    def Changeselcteditemcolor(self, item):
        if self.currentItem is not None:
            if self.currentItem.type == 0:
                self.currentItem.setBrush(self.NOTHING_COLOR)
                idx = self.bndboxList.index(self.currentItem)
                self.idList[idx].setDefaultTextColor(QColor(Qt.red))
            elif self.currentItem.type == 1:
                self.currentItem.setBrush(self.NOTHING_COLOR)
                idx = self.bndboxList.index(self.currentItem)
                self.idList[idx].setDefaultTextColor(QColor(Qt.red))
            elif self.currentItem.type == 2:
                self.symbol_line_scene.removeItem(self.line_Box)
                idx = self.lineList.index(self.currentItem)
                # 아이디 색 변화
                idx_id = self.lineList.index(self.currentItem) + len(self.bndboxList)
                self.idList[idx_id].setDefaultTextColor(QColor(Qt.blue))
                # arrow 색 변화
                arrow_data = self.arrowList[idx]
                for i in range(0, len(arrow_data)):
                    arrow_data[i].setBrush(self.NOTHING_COLOR)
            elif self.currentItem.type == 3:
                self.symbol_line_scene.removeItem(self.line_Box)
                # arrow 색 변화
                for idx in range(0,len(self.arrowList)):
                    if self.currentItem in self.arrowList[idx]:
                        break
                arrow_data = self.arrowList[idx]
                for i in range(0, len(arrow_data)):
                    arrow_data[i].setBrush(self.NOTHING_COLOR)
                # 아이디 색 변화
                idx_id = idx + len(self.bndboxList)
                self.idList[idx_id].setDefaultTextColor(QColor(Qt.blue))
        self.currentItem = item
        self.currentItem.setBrush(self.SELECTED_COLOR)
        # 아이디 색 변화
        idx = self.bndboxList.index(self.currentItem)
        self.idList[idx].setDefaultTextColor(QColor(Qt.green))
         

    def Changeselcteditemcolorline(self, item):
        if self.currentItem is not None:
            if self.currentItem.type == 0:
                self.currentItem.setBrush(self.NOTHING_COLOR)
                idx = self.bndboxList.index(self.currentItem)
                self.idList[idx].setDefaultTextColor(QColor(Qt.red))
            elif self.currentItem.type == 1:
                self.currentItem.setBrush(self.NOTHING_COLOR)
                idx = self.bndboxList.index(self.currentItem)
                self.idList[idx].setDefaultTextColor(QColor(Qt.red))
            elif self.currentItem.type == 2:
                self.symbol_line_scene.removeItem(self.line_Box)
                idx = self.lineList.index(self.currentItem)
                # 아이디 색 변화
                idx_id = self.lineList.index(self.currentItem) + len(self.bndboxList)
                self.idList[idx_id].setDefaultTextColor(QColor(Qt.blue))
                # arrow 색 변화
                arrow_data = self.arrowList[idx]
                for i in range(0, len(arrow_data)):
                    arrow_data[i].setBrush(self.NOTHING_COLOR)
            elif self.currentItem.type == 3:
                self.symbol_line_scene.removeItem(self.line_Box)
                # arrow 색 변화
                for idx in range(0,len(self.arrowList)):
                    if self.currentItem in self.arrowList[idx]:
                        break
                arrow_data = self.arrowList[idx]
                for i in range(0, len(arrow_data)):
                    arrow_data[i].setBrush(self.NOTHING_COLOR)
                # 아이디 색 변화
                idx_id = idx + len(self.bndboxList)
                self.idList[idx_id].setDefaultTextColor(QColor(Qt.blue))
        self.currentItem = item
        # 바운딩 박스 생성
        if self.currentItem.type == 2:
            # 좌표값
            line_start = self.currentItem.line().p1()
            line_end = self.currentItem.line().p2()

            if (line_start.x() == line_end.x()) | (line_start.y() == line_end.y()):
                line_Box = self.currentItem.boundingRect()
                self.line_Box = QGraphicsRectItem(line_Box)
                
            else:
                length = ((line_start.x() - line_end.x())**2 + (line_start.y() - line_end.y())**2)**0.5
                rect_x = (line_start.x() + line_end.x())/2 - length/2
                rect_y = (line_start.y() + line_end.y())/2 - 5
                line_box = QRectF(rect_x, rect_y, length, 10)                
                self.line_Box = QGraphicsRectItem(line_box)

                # 회전
                center = line_box.center()
                transform = QTransform()
                theta = math.degrees(math.atan((line_end.y()-line_start.y())/(line_end.x()-line_start.x())))
                if theta < 0:
                    transform.translate(center.x(), center.y())
                    transform.rotate(theta)
                    transform.translate(-center.x(), -center.y())
                else:
                    transform.translate(center.x(), center.y())
                    transform.rotate(theta)
                    transform.translate(-center.x(), -center.y())
                self.line_Box.setTransform(transform)
                
            self.line_Box.setBrush(self.SELECTED_COLOR)
            self.symbol_line_scene.addItem(self.line_Box)

        elif self.currentItem.type == 3:
            for idx in range(0,len(self.arrowList)):
                if self.currentItem in self.arrowList[idx]:
                    break
            line_start = self.lineList[idx].line().p1()
            line_end = self.lineList[idx].line().p2()

            if (line_start.x() == line_end.x()) | (line_start.y() == line_end.y()):
                line_Box = self.lineList[idx].boundingRect()
                self.line_Box = QGraphicsRectItem(line_Box)
                
            else:
                length = ((line_start.x() - line_end.x())**2 + (line_start.y() - line_end.y())**2)**0.5
                rect_x = (line_start.x() + line_end.x())/2 - length/2
                rect_y = (line_start.y() + line_end.y())/2 - 5
                line_box = QRectF(rect_x, rect_y, length, 10)                
                self.line_Box = QGraphicsRectItem(line_box)

                # 회전
                center = line_box.center()
                transform = QTransform()
                theta = math.degrees(math.atan((line_end.y()-line_start.y())/(line_end.x()-line_start.x())))
                print(theta)
                if theta < 0:
                    transform.translate(center.x(), center.y())
                    transform.rotate(theta)
                    transform.translate(-center.x(), -center.y())
                else:
                    transform.translate(center.x(), center.y())
                    transform.rotate(theta)
                    transform.translate(-center.x(), -center.y())
                self.line_Box.setTransform(transform)
            self.line_Box.setBrush(self.SELECTED_COLOR)
            self.symbol_line_scene.addItem(self.line_Box)
        
        # 색 변화
        if self.currentItem in self.lineList:
            idx = self.lineList.index(self.currentItem)
            arrow_data = self.arrowList[idx]
            for i in range(0, len(arrow_data)):
                arrow_data[i].setBrush(self.SELECTED_COLOR)
            idx_id = idx + len(self.bndboxList)
            self.idList[idx_id].setDefaultTextColor(QColor(Qt.green))
        else:
            for idx in range(0,len(self.arrowList)):
                if self.currentItem in self.arrowList[idx]:
                    break
            arrow_data = self.arrowList[idx]
            for i in range(0, len(arrow_data)):
                arrow_data[i].setBrush(self.SELECTED_COLOR)
            idx_id = idx + len(self.bndboxList)
            self.idList[idx_id].setDefaultTextColor(QColor(Qt.green))


    def wheelEvent(self, event):
        zoomInFactor = 1.25
        zoomOutFactor = 1 / zoomInFactor

        # Set Anchors
        self.setTransformationAnchor(self.NoAnchor)
        self.setResizeAnchor(self.NoAnchor)

        # Save the scene pos
        # QGraphicsView나 QGraphicsScene 내의 좌표를 해당 뷰 또는 scene의 좌표 공간으로 변환해주는 메서드
        oldPos = self.mapToScene(event.pos())         

        # Zoom
        if event.angleDelta().y() > 0:
            zoomFactor = zoomInFactor
            if self.zoomInCnt < 3:
                self.zoomInCnt += 1
                self.scale(zoomFactor, zoomFactor)
                self.zoomOutCnt -= 1
        else:
            zoomFactor = zoomOutFactor
            if self.zoomOutCnt <= 10:
                self.zoomOutCnt += 1
                self.scale(zoomFactor, zoomFactor)
                self.zoomInCnt -= 1

        # Get the new position
        newPos = self.mapToScene(event.pos())

        # Move scene to old position
        delta = newPos - oldPos
        self.translate(delta.x(), delta.y())


    def Show_object(self, symbol, text, line, arrow, id):
        # id_num = len(self.idList)
        if symbol:
            for box in self.bndboxList:
                if box.type:
                    self.Symbol_on(box)
            if  text:       
                for box in self.bndboxList:
                    if not box.type:
                        self.Text_On(box)
                if line:
                    for idx in range(0,len(self.lineList)):
                        self.Line_color_set(idx)
                    if arrow:
                        for arrowlist in self.arrowList:
                            for box in arrowlist:
                                self.Arrow_on(box)
                        if id:
                            for text in self.idList:
                                self.Id_on(text)
                        else:
                            for text in self.idList:
                                self.Off_id(text)
                    else:
                        for arrowlist in self.arrowList:
                            for box in arrowlist:
                                self.Off(box)
                        if id:
                            for text in self.idList:
                                self.Id_on(text)
                        else:
                            for text in self.idList:
                                self.Off_id(text)
                else:
                    for line in self.lineList:
                        self.Off(line)
                    if arrow:
                        for arrowlist in self.arrowList:
                            for box in arrowlist:
                                self.Arrow_on(box)
                        if id:
                            for text in self.idList:
                                self.Id_on(text)
                        else:
                            for text in self.idList:
                                self.Off_id(text)
                    else:
                        for arrowlist in self.arrowList:
                            for box in arrowlist:
                                self.Off(box)
                        if id:
                            for text in self.idList:
                                self.Id_on(text)
                        else:
                            for text in self.idList:
                                self.Off_id(text)
            else:
                for box in self.bndboxList:
                    if not box.type:
                        self.Off(box)
                if line:
                    for idx in range(0,len(self.lineList)):
                        self.Line_color_set(idx)
                    if arrow:
                        for arrowlist in self.arrowList:
                            for box in arrowlist:
                                self.Arrow_on(box)
                        if id:
                            for text in self.idList:
                                self.Id_on(text)
                        else:
                            for text in self.idList:
                                self.Off_id(text)
                    else:
                        for arrowlist in self.arrowList:
                            for box in arrowlist:
                                self.Off(box)
                        if id:
                            for text in self.idList:
                                self.Id_on(text)
                        else:
                            for text in self.idList:
                                self.Off_id(text)
                else:
                    for line in self.lineList:
                        self.Off(line)
                    if arrow:
                        for arrowlist in self.arrowList:
                            for box in arrowlist:
                                self.Arrow_on(box)
                        if id:
                            for text in self.idList:
                                self.Id_on(text)
                        else:
                            for text in self.idList:
                                self.Off_id(text)
                    else:
                        for arrowlist in self.arrowList:
                            for box in arrowlist:
                                self.Off(box)
                        if id:
                            for text in self.idList:
                                self.Id_on(text)
                        else:
                            for text in self.idList:
                                self.Off_id(text)
        
        else:
            for box in self.bndboxList:
                if box.type:
                    self.Off(box)
            if  text:       
                for box in self.bndboxList:
                    if not box.type:
                        self.Text_On(box)
                if line:
                    for idx in range(0,len(self.lineList)):
                        self.Line_color_set(idx)
                    if arrow:
                        for arrowlist in self.arrowList:
                            for box in arrowlist:
                                self.Arrow_on(box)
                        if id:
                            for text in self.idList:
                                self.Id_on(text)
                        else:
                            for text in self.idList:
                                self.Off_id(text)
                    else:
                        for arrowlist in self.arrowList:
                            for box in arrowlist:
                                self.Off(box)
                        if id:
                            for text in self.idList:
                                self.Id_on(text)
                        else:
                            for text in self.idList:
                                self.Off_id(text)
                else:
                    for line in self.lineList:
                        self.Off(line)
                    if arrow:
                        for arrowlist in self.arrowList:
                            for box in arrowlist:
                                self.Arrow_on(box)
                        if id:
                            for text in self.idList:
                                self.Id_on(text)
                        else:
                            for text in self.idList:
                                self.Off_id(text)
                    else:
                        for arrowlist in self.arrowList:
                            for box in arrowlist:
                                self.Off(box)
                        if id:
                            for text in self.idList:
                                self.Id_on(text)
                        else:
                            for text in self.idList:
                                self.Off_id(text)
            else:
                for box in self.bndboxList:
                    if not box.type:
                        self.Off(box)
                if line:
                    for idx in range(0,len(self.lineList)):
                        self.Line_color_set(idx)
                    if arrow:
                        for arrowlist in self.arrowList:
                            for box in arrowlist:
                                self.Arrow_on(box)
                        if id:
                            for text in self.idList:
                                self.Id_on(text)
                        else:
                            for text in self.idList:
                                self.Off_id(text)
                    else:
                        for arrowlist in self.arrowList:
                            for box in arrowlist:
                                self.Off(box)
                        if id:
                            for text in self.idList:
                                self.Id_on(text)
                        else:
                            for text in self.idList:
                                self.Off_id(text)
                else:
                    for line in self.lineList:
                        self.Off(line)
                    if arrow:
                        for arrowlist in self.arrowList:
                            for box in arrowlist:
                                self.Arrow_on(box)
                        if id:
                            for text in self.idList:
                                self.Id_on(text)
                        else:
                            for text in self.idList:
                                self.Off_id(text)
                    else:
                        for arrowlist in self.arrowList:
                            for box in arrowlist:
                                self.Off(box)
                        if id:
                            for text in self.idList:
                                self.Id_on(text)
                        else:
                            for text in self.idList:
                                self.Off_id(text)
    
    
    def Text_On(self, box):
        pen = QPen(Qt.red)
        pen.setWidth(3)
        box.setPen(pen)
    def Symbol_on(self, box):
        pen = QPen(Qt.green)
        pen.setWidth(3)
        box.setPen(pen)
    def Arrow_on(self, box):
        pen = QPen(QColor(255, 130, 36))
        pen.setWidth(3)
        box.setPen(pen)
    def Id_on(self, box):
        if box.type == 4:
            box.setDefaultTextColor(QColor(Qt.red))
        elif box.type == 5:
            box.setDefaultTextColor(QColor(Qt.blue))
    def Off(self, object):
        pen = QPen(Qt.transparent)
        pen.setWidth(3)
        object.setPen(pen)
    def Off_id(self, object):
        object.setDefaultTextColor(QColor(Qt.transparent))
                  

    def Line_color_set(self, idx):
        line_object = self.lineList[idx]
        line_data = self.line_data[idx][0]
        if (line_data=='continuous_thick_line') or (line_data=='continuous_line'):
            pen = QPen(QColor(92, 209, 229, 150))
            pen.setWidth(10)
            line_object.setPen(pen)
        elif line_data=='specbreaker_line':
            pen = QPen(QColor(0, 0, 255, 150))
            pen.setWidth(10)
            line_object.setPen(pen)
        elif (line_data=='dimension_line') or (line_data=='extension_line'):
            pen = QPen(QColor(255, 255, 54, 150))
            pen.setWidth(10)
            line_object.setPen(pen)
        elif line_data=='annotation_line':
            pen = QPen(QColor(255, 108, 235, 150))
            pen.setWidth(10)
            line_object.setPen(pen)
        elif line_data=='leader_line':
            pen = QPen(QColor(29, 219, 22, 150))
            pen.setWidth(10)
            line_object.setPen(pen)
        elif line_data=='short_dotted_line':
            pen = QPen(QColor(153, 0, 76, 150))
            pen.setWidth(10)
            line_object.setPen(pen)
        else:
            pen = QPen(QColor(237, 0, 203, 150))
            pen.setWidth(10)
            line_object.setPen(pen)
        arrow_box = self.arrowList[idx]
        for i in range(0, len(arrow_box)):
            pen = QPen(QColor(255, 130, 36))
            pen.setWidth(3)
            arrow_box[i].setPen(pen)


class GraphicsScene(QGraphicsScene):
    def __init__(self, bndBoxList, lineList, arrowList):
        super().__init__()

        # 변수 초기화
        self.backImg = ''
        self._start = QPointF()
        self._end = QPointF()
        self.isExistingBox = None
        self.isExistingline = None
        self.selectedItem = None
        self.isAdding = False
        self.drag_start = QPointF()
        self.on_selected = None
        self.bndBoxList = bndBoxList            # From QGraphicsView
        self.arrowList = arrowList
        self.lineList = lineList
        self.changeSelectedItemColor = None     # From QGraphicsView
        self.changeSelectedItemColorLine = None


    def Set_image(self, img_path):
        # 이미지를 QPixmap 객체로 표현
        self.backImg = QPixmap(img_path)

        # 이미지를 표시
        graphicsPixmapItem = QGraphicsPixmapItem(self.backImg)
        self.addItem(graphicsPixmapItem)


    def mousePressEvent(self, event):
        self.isExistingBox = isinstance(self.itemAt(event.scenePos(), QTransform()), QGraphicsRectItem)
        self.isExistingline = isinstance(self.itemAt(event.scenePos(), QTransform()), QGraphicsLineItem)

        # 존재하는 박스 클릭 시
        if self.isExistingBox:
            self.selectedItem = self.itemAt(event.scenePos(), QTransform())
            if self.selectedItem in self.bndBoxList:
                self.on_selected(self.bndBoxList.index(self.selectedItem))
                self.changeSelectedItemColor(self.selectedItem)
            else:
                pass

            for idx in range(0,len(self.arrowList)):
                if self.selectedItem in self.arrowList[idx]:
                    self.on_selected(idx)
                    self.changeSelectedItemColorLine(self.selectedItem)
                else:
                    pass

        # 존재하는 라인 클릭 시
        elif self.isExistingline:
            self.selectedItem = self.itemAt(event.scenePos(), QTransform())
            self.on_selected(self.lineList.index(self.selectedItem))
            self.changeSelectedItemColorLine(self.selectedItem)
        else:
            # 마우스 클릭 시 포인트 생성
            if event.button() == 1:
                mouse_position = event.pos()

                # Create a QPoint object from the mouse click position
                self.drag_start = QPointF(mouse_position.x(), mouse_position.y())


#----------------------------------------------------------객체 정의----------------------------------------------------------
class BoundingBox(QGraphicsRectItem):
    def __init__(self, isInitData=True, type=None):
        super().__init__()
        self.isInitData = isInitData

        # 0: Text / 1: Symbol
        self.type = type


class BoundingLine(QGraphicsLineItem):
    def __init__(self, isInitData=True):
        super().__init__()
        self.isInitData = isInitData

        # 2: Line
        self.type = 2


#----------------------------------------------------------View 객체와 Table 객체를 연동----------------------------------------------------------
class SceneViewModel:
    def __init__(self, symbol_model, line_model, view):
        super().__init__()
        self.selectedDataIndex = None

        # 모델 객체 이용 (Symbol)
        self.model = symbol_model
        self.model.setLayerSignal(notify_selected_to_layer=self.get_selected_index)

        self.model2 = line_model
        self.model2.setLayerSignalLine(notify_selected_to_layer=self.get_selected_index)
        
        self.layerView = view

        self.layerView.Setsignal(get_data_func=self.getBoxData, notify_selected_index=self.notify_selected_index, get_data_func_line=self.getLineData)
        
        self.layerView.Setinitdata()
        self.layerView.Setinitdataline()
        self.layerView.Id_rect()

    #-------------------------------------------------------------------------------------------------------------------------
    # Setsignal 하위
    def getBoxData(self):
        return self.model.getBoxData()
    

    def getLineData(self):
        return self.model2.getLineData()


    # Setsignal 하위
    def notify_selected_index(self, i):
        if self.layerView.symbol_line_scene.isExistingBox:
            if self.layerView.symbol_line_scene.selectedItem in self.layerView.symbol_line_scene.bndBoxList:
                self.model.setSelectedDataIndex(i, 0)
            for idx in range(0,len(self.layerView.arrowList)):
                if self.layerView.symbol_line_scene.selectedItem in self.layerView.symbol_line_scene.arrowList[idx]:
                    self.model2.setSelectedDataIndexLine(i, 0)
                    break
        elif self.layerView.symbol_line_scene.isExistingline:
            self.model2.setSelectedDataIndexLine(i, 0)


    # setLayerSignal 하위
    def get_selected_index(self, idx):
        if self.model.check:
            self.selectedIndex = idx
            self.layerView.Selectionchange(self.selectedIndex)
        elif not self.model.check:
            self.selectedIndex = idx
            self.layerView.Selectionchangeline(self.selectedIndex)