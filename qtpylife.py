#!/usr/bin/env python3

import sys
import random
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QMainWindow, QAction, qApp, QStyle
from PyQt5.QtGui import QPainter, QColor, QIcon
from PyQt5.QtCore import QBasicTimer
from itertools import product

'''
File: qtpylife.py
Description: an implementation of Conway's Game of Life in PyQt5
Author: tetrismegistus
Version .01 -- Initial Commit 12/27/17 tetrismegistus
Version .02 -- use permutations for neighbor finding code
'''


class Cell(QWidget):
    def __init__(self):
        # noinspection PyArgumentList
        super().__init__()
        self.color = 'white'
        self.alive = 0
        self.live_neighbors = 0

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_rectangles(qp)
        qp.end()

    def draw_rectangles(self, qp):

        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')
        qp.setPen(col)
        qp.setBrush(QColor(self.color))
        qp.drawRect(0, 0, 15, 15)

    def mousePressEvent(self, event):

        self.change_state()

    def change_state(self):
        if self.alive:
            self.color = 'white'
            self.alive = 0
        else:
            self.color = 'red'
            self.alive = 1
        self.update()

    def check_health(self):
        if self.live_neighbors < 2 and self.alive:
            self.change_state()
        elif self.live_neighbors in range(2, 3) and self.alive:
            pass
        elif self.live_neighbors > 3 and self.alive:
            self.change_state()
        elif self.live_neighbors == 3 and not self.alive:
            self.change_state()
        else:
            pass


# noinspection PyArgumentList
class Board(QWidget):
    def __init__(self):
        super().__init__()
        self.grid = QGridLayout()
        self.grid.setSpacing(0)

        self.setLayout(self.grid)
        self.size_x = 30
        self.size_y = 30
        board = [(i, j) for i in range(self.size_x) for j in range(self.size_y)]
        for position in board:
            cell = Cell()
            self.grid.addWidget(cell, *position)
        self.timer = QBasicTimer()
        self.running = False

    def timerEvent(self, e):
        for i in range(self.grid.count()):
            layout_item = self.grid.itemAt(i)
            position = self.grid.getItemPosition(i)
            x, y = position[0], position[1]
            cell = layout_item.widget()
            self.count_neighbors(x, y, cell)

        for i in range(self.grid.count()):
            layout_item = self.grid.itemAt(i)
            cell = layout_item.widget()
            cell.check_health()

    def random_fill(self):
        for i in range(self.grid.count()):
            flip = random.randint(0, 1)
            if flip:
                layout_item = self.grid.itemAt(i)
                cell = layout_item.widget()
                cell.change_state()

    def count_neighbors(self, x, y, cell_to_analyze):

        operations = [[], []]
        neighbors = 0

        for operation in range(-1, 2):
            operations[0].append((x + operation) % self.size_x)
            operations[1].append((y + operation) % self.size_y)

        coord_list = list(product(operations[0], operations[1]))  # create list of permutations of values
        coord_list.remove((x, y))  # prevent cell from counting its self as a neighbor

        for coord in coord_list:
            # pdb.set_trace()
            neighbors += self.grid.itemAtPosition(coord[0], coord[1]).widget().alive

        cell_to_analyze.live_neighbors = neighbors

    def timer_start(self):
        self.timer.start(100, self)


# noinspection PyArgumentList
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        board = Board()
        self.setCentralWidget(board)
        size_x = self.centralWidget().size_x
        size_y = self.centralWidget().size_y
        self.setGeometry(300, 300, 15 * size_x, 15 * size_y)
        self.setFixedSize(15 * size_x, 15 * size_y)
        self.setWindowTitle('Game of Life')
        self.toolbar = self.addToolBar('Main')
        self.style = self.style()
        self.play_icon = self.style.standardIcon(QStyle.SP_MediaPlay)
        self.stop_icon = self.style.standardIcon(QStyle.SP_MediaStop)
        self.build_toolbar()
        self.setWindowIcon(QIcon('glider.png'))
        self.show()

    # noinspection PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences
    def build_toolbar(self):
        exit_action = QAction(QIcon('exit.png'), 'Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(qApp.quit)
        self.toolbar.addAction(exit_action)

        # noinspection PyAttributeOutsideInit
        self.timer_toggle = QAction(QIcon(self.play_icon), 'Play', self)
        self.timer_toggle.setShortcut('Ctrl+S')
        self.timer_toggle.triggered.connect(self.timer_switch)
        self.toolbar.addAction(self.timer_toggle)

        random_fill = QAction(QIcon(self.style.standardIcon(QStyle.SP_MessageBoxQuestion)), 'Random Fill', self)
        random_fill.setShortcut('Ctrl+R')
        random_fill.triggered.connect(self.centralWidget().random_fill)
        self.toolbar.addAction(random_fill)

    def timer_switch(self):
        if self.centralWidget().running:
            self.timer_toggle.setIcon(self.play_icon)
            self.timer_toggle.setText('Play')
            self.centralWidget().timer.stop()
            self.centralWidget().running = False
        else:
            self.timer_toggle.setIcon(self.stop_icon)
            self.timer_toggle.setText('Stop')
            self.centralWidget().timer_start()
            self.centralWidget().running = True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
