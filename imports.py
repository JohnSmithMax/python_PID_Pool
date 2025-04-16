import sys
import time
from collections import deque

# Импорты из PyQt5
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSlider,
    QLabel,
    QCheckBox,
    QFrame
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath