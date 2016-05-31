from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtCore import QRectF

class Area(QGraphicsScene):
    def mousePressEvent(self, e):
        self.start_x = e.scenePos().x();
        self.start_y = e.scenePos().y();


    def mouseReleaseEvent(self, e):
        self.end_x = e.scenePos().x();
        self.end_y = e.scenePos().y();
        self.addRect(QRectF(self.start_x, self.start_y, self.end_y-self.start_y, self.end_x-self.start_x));