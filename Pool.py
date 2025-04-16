from imports import *
from definitions import *
class Pool(QWidget):
    def __init__(self):
        super().__init__()
        self.water_level = START_WATER_LEVEL
        self.inflow_rate = 0
        self.outflow_rate = 0

    def paintEvent(self, event):
        width = self.width()
        height = self.height()

        painter = QPainter(self)

        # Рассчитываем пропорциональные размеры
        pool_margin = int(min(width, height) * 0.05)  # 5% от меньшей стороны
        pool_width = int(width - 2 * pool_margin)
        pool_height = int(height - 2 * pool_margin)

        # Координаты бассейна
        pool_left = pool_margin
        pool_top = pool_margin
        pool_right = pool_left + pool_width
        pool_bottom = pool_top + pool_height

        # Рисуем бассейн (зеленый прямоугольник)
        painter.setPen(QPen(QColor(0, 100, 0), 2))
        painter.setBrush(QColor(200, 255, 200))
        painter.drawRect(pool_left, pool_top, pool_width, pool_height)

        # Рисуем воду (синий прямоугольник)
        water_height = int(pool_height * self.water_level / 100)
        painter.setPen(QPen(QColor(0, 0, 150), 1))
        painter.setBrush(QColor(100, 100, 255))
        painter.drawRect(pool_left, pool_bottom - water_height, pool_width, water_height)

        # Линия целевого уровня
        target_height = int(pool_height * TARGET_POOL_LEVEL / 100)
        painter.setPen(QPen(Qt.red, 2, Qt.DashLine))
        painter.drawLine(pool_left, pool_bottom - target_height,
                         pool_right, pool_bottom - target_height)

        # Рисуем трубы
        pipe_thickness = max(2, min(width, height) * 0.01)

        # Труба наполнения (слева, синяя)
        pipe_in_y = int(pool_top + pool_height * 0.2)
        painter.setPen(QPen(QColor(0, 0, 255), pipe_thickness))
        painter.drawLine(int(pool_left - pool_margin * 0.8), pipe_in_y,
                         pool_left, pipe_in_y)
        painter.drawText(int(pool_left - pool_margin * 0.8), pipe_in_y - 5,
                         f"IN: {self.inflow_rate:.1f}")

        # Труба слива (справа, красная)
        pipe_out_y = int(pool_top + pool_height * 0.6)
        painter.setPen(QPen(QColor(255, 0, 0), pipe_thickness))
        painter.drawLine(pool_right, pipe_out_y,
                         int(pool_right + pool_margin * 0.8), pipe_out_y)
        painter.drawText(int(pool_right - pool_margin * 2), pipe_out_y - 5,
                         f"OUT: {self.outflow_rate:.1f}")

        # Отображаем уровень воды
        font_size = int(max(10, min(width, height) * 0.03))
        font = painter.font()
        font.setPixelSize(int(font_size))
        painter.setFont(font)

        painter.setPen(QPen(Qt.black, 1))
        painter.drawText(width // 2 - 50, pool_top - 10,
                         f"Уровень воды: {self.water_level:.1f}%")

    def update_water_level(self):
        # Обновляем уровень воды в зависимости от потоков
        delta = self.inflow_rate - self.outflow_rate
        self.water_level += delta * 0.1

        # Ограничиваем уровень воды
        self.water_level = max(0, min(MAX_POOL_LEVEL, self.water_level))
        self.update()