from imports import *
from definitions import *
from PIDController import PIDController
from Pool import Pool
from WaterLevelGraph import WaterLevelGraph

class HMIWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)

        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Создаем ПИД-регулятор
        self.pid = PIDController(Kp=KP, Ki=KI, Kd=KD, setpoint=TARGET_POOL_LEVEL)
        self.pid_enabled = PID_ENABLED

        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Основной вертикальный layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Горизонтальный layout для бассейна и графика
        pool_graph_layout = QHBoxLayout()
        main_layout.addLayout(pool_graph_layout, stretch=4)

        # Виджет для отображения бассейна (слева)
        self.pool_widget = Pool()
        pool_graph_layout.addWidget(self.pool_widget, stretch=1)

        # График уровня воды (справа)
        self.water_graph = WaterLevelGraph()
        pool_graph_layout.addWidget(self.water_graph, stretch=1)

        # Разделительная линия
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(separator)

        # Панель управления
        control_layout = QHBoxLayout()
        main_layout.addLayout(control_layout)

        # Управление трубой наполнения
        inflow_layout = QVBoxLayout()
        inflow_label = QLabel(INFLOW_PIPE)
        self.inflow_slider = QSlider(Qt.Horizontal)
        self.inflow_slider.setRange(MIN_SLIDER, MAX_INFLOW_SLIDER)
        self.inflow_slider.valueChanged.connect(self.update_inflow)
        inflow_layout.addWidget(inflow_label, stretch=1)
        inflow_layout.addWidget(self.inflow_slider)
        control_layout.addLayout(inflow_layout)

        # Управление трубой слива
        outflow_layout = QVBoxLayout()
        outflow_label = QLabel(OUTFLOW_PIPE)
        self.outflow_slider = QSlider(Qt.Horizontal)
        self.outflow_slider.setRange(MIN_SLIDER, MAX_OUTFLOW_SLIDER)
        self.outflow_slider.valueChanged.connect(self.update_outflow)
        outflow_layout.addWidget(outflow_label)
        outflow_layout.addWidget(self.outflow_slider)
        control_layout.addLayout(outflow_layout)

        # Панель ПИД-регулятора
        pid_layout = QVBoxLayout()

        # Чекбокс для включения/выключения ПИД-регулятора
        self.pid_checkbox = QCheckBox(PID_CHECKBOX_LABEL)
        self.pid_checkbox.stateChanged.connect(self.toggle_pid)
        pid_layout.addWidget(self.pid_checkbox)

        # Кнопка сброса
        reset_button = QPushButton(RESET_SYSTEM)
        reset_button.clicked.connect(self.reset_system)
        pid_layout.addWidget(reset_button)

        main_layout.addLayout(pid_layout)

        # Таймер для обновления уровня воды
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_system)
        self.timer.start(UPDATE_TIMER_MS)

        self.update_graph_timer = QTimer()
        self.update_graph_timer.timeout.connect(self.update_graph)
        self.update_graph_timer.start(GRAPH_UPDATE_INTERVAL_MS)

    def update_inflow(self, value):
        self.pool_widget.inflow_rate = value

    def update_outflow(self, value):
        self.pool_widget.outflow_rate = value

    def toggle_pid(self, state):
        self.pid_enabled = state == Qt.Checked
        if self.pid_enabled:
            # Сброс интегральной составляющей при включении ПИД
            self.pid.integral = RESET_INTEGRAL_TO_START
            self.pid.last_error = RESET_INTEGRAL_TO_START
            self.pool_widget.outflow_rate = self.outflow_slider.value()
    def update_graph(self):
        self.water_graph.add_data_point(self.pool_widget.water_level)

    def update_system(self):
        if self.pid_enabled:
            # Вычисляем управляющее воздействие ПИД-регулятора
            pid_output = self.pid.compute(self.pool_widget.water_level)

            # Применяем управляющее воздействие к трубе наполнения
            self.pool_widget.inflow_rate = pid_output
            self.inflow_slider.setValue(int(pid_output))

            self.pool_widget.outflow_rate = self.outflow_slider.value()

        # Обновляем уровень воды
        self.pool_widget.update_water_level()

    def reset_system(self):
        self.pool_widget.water_level = POOL_DEFAULT_LEVEL
        self.inflow_slider.setValue(MIN_SLIDER)
        self.outflow_slider.setValue(MIN_SLIDER)
        self.pid_checkbox.setChecked(False)
        self.pid.integral = RESET_INTEGRAL_TO_START
        self.pid.last_error = RESET_INTEGRAL_TO_START
        self.pool_widget.update()
        self.pool_widget.outflow_rate = OUTFLOW_RATE
        self.outflow_slider.setValue(OUTFLOW_RATE)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HMIWindow()
    window.show()
    window.reset_system()
    sys.exit(app.exec_())