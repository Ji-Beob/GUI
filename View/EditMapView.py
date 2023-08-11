from Window.MainWindow import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QBrush

class graphicsView(QGraphicsView):                                  # QGraphicsView: 만들어지는 인스턴스는 QGraphicsScene을 표시하기 위한 뷰
    def __init__(self, imgPath):
        super().__init__()

        self.setBackgroundBrush(QBrush(Qt.white, Qt.SolidPattern))

        # self.scene = GraphicsScene()
        self.scene.set_image(img_path = imgPath)
        self.setScene(self.scene)

        self.zoomInCnt = 0
        self.zoomOutCnt = 0

    # 선택동작 활성화 또는 비활성화
    def selectActivate(self, flag, state):
        if flag == 'except' and state == True:
            self.scene.exceptActive = True
            self.scene.outlineActive = False
        elif flag == 'except' and state == False:
            self.scene.exceptActive = False
        elif flag == 'outline' and state == True:
            self.scene.outlineActive = True
            self.scene.exceptActive = False
        else:
            self.scene.outlineActive = False


    def wheelEvent(self, event):
        zoomInFactor = 1.25                                         # 줌 인 배율 계수
        zoomOutFactor = 1 / zoomInFactor                            # 줌 아웃 배율 계수

        # Set Anchors
        self.setTransformationAnchor(self.NoAnchor)
        self.setResizeAnchor(self.NoAnchor)

        # Save the scene pos
        oldPos = self.mapToScene(event.pos())                       # 이전 scene의 좌표를 저장

        # Zoom
        if event.angleDelta().y() > 0:
            zoomFactor = zoomInFactor
            if self.zoomInCnt < 3:                                  # 줌 카운트가 3보다 작을 때만 줌을 시행
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

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setDragMode(self.ScrollHandDrag)
        super(graphicsView, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setDragMode(self.NoDrag)
        super(graphicsView, self).mouseReleaseEvent(event)

