from imports import *
from definitions import *

class WaterLevelGraph(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(GRAPH_MINIMUM_HEIGHT)
        self.water_levels = deque(maxlen=GRAPH_MAX_POINTS)
        self.target_level = TARGET_POOL_LEVEL

    def add_data_point(self, level):
        self.water_levels.append(level)
        self.update()

    def paintEvent(self, event):
        width = self.width()
        height = self.height()
        painter = QPainter(self)

        # Рассчитываем пропорциональные размеры
        margin = int(min(width, height) * 0.05)
        graph_width = width - 2 * margin
        graph_height = height - 2 * margin

        # Координаты графика
        graph_left = margin
        graph_top = margin
        graph_right = graph_left + graph_width
        graph_bottom = graph_top + graph_height

        # Рисуем фон
        painter.fillRect(graph_left, graph_top, graph_width, graph_height,
                         QColor(*GRAPH_BG_COLOR))

        # Рисуем оси
        axis_thickness = max(1, min(width, height) * 0.005)
        painter.setPen(QPen(Qt.black, axis_thickness))

        # Вертикальная ось (с подписями)
        painter.drawLine(graph_left, graph_top, graph_left, graph_bottom)
        font_size = int(max(10, min(width, height) * 0.025))
        font = painter.font()
        font.setPixelSize(font_size)
        painter.setFont(font)

        painter.drawText(int(graph_left + 5), graph_top + 10, "100%")
        painter.drawText(int(graph_left + 5), (graph_top + graph_bottom) // 2, "50%")
        painter.drawText(int(graph_left + 5), graph_bottom - 5, "0%")

        # Горизонтальная ось (время)
        painter.drawLine(graph_left, graph_bottom, graph_right, graph_bottom)

        # Линия целевого уровня
        target_y = graph_bottom - int(graph_height * self.target_level / 100)
        painter.setPen(QPen(QColor(*TARGET_LINE_COLOR), axis_thickness, Qt.DashLine))
        painter.drawLine(graph_left, target_y, graph_right, target_y)
        painter.drawText(graph_right - int(margin * 1.5), target_y - 5,
                         f"{self.target_level}%")

        if len(self.water_levels) > 0:
            lastX = graph_left
            lastY = graph_top
            for index, value in enumerate(self.water_levels):
                kx = graph_width / GRAPH_MAX_POINTS
                ky = graph_height / MAX_POOL_LEVEL
                firstX = int(index * kx + graph_left)
                firstY = int(graph_height - value * ky + graph_top)
                q = QPainter()
                q.begin(self)
                q.drawLine(lastX, lastY, firstX, firstY)
                q.end()
                lastX = firstX
                lastY = firstY