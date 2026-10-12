"""Зачётный проект: «Каталог книг» (PySide6)."""
import sys
from abc import ABC, abstractmethod
from datetime import datetime
from functools import total_ordering

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QApplication, QComboBox, QDialog, QGridLayout, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow, QMessageBox, QPushButton,
    QSpinBox, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget,
    QAbstractItemView,

