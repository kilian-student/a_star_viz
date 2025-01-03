from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.axes import Axes

from typing import Optional

from utils.a_start_algorithm import A_star
from PyQt5.QtCore import pyqtSignal, QObject

class MatplotlibWidget(QWidget):
    """Widget for handling the matplotlib graph visualization. Calls the plot_graph function from the algorithm.

    Args:
        QWidget (_type_): parent widget
    """
    def __init__(self, parent=None, signal: Optional[QObject] = None):
        super().__init__(parent)

        # create algorithm instance
        self.algorithm = A_star()

        # Create a Matplotlib figure
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self._ax: Optional[Axes] = None

        # Connect the click event
        self.clicked_signal = signal
        self.figure.canvas.mpl_connect("button_press_event", self.on_click)


        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # Initialize the plot
        self.init_graph_widget()

    def on_click(self, event):
        print('user click event detected')
        if event.inaxes == self._ax:  # Ensure click is inside the plot
            print(f'click pos: {event.xdata}, {event.ydata}')
            for node in self.algorithm.graph.nodes:
                if abs(event.xdata - node.pos.x) < 0.5 and abs(event.ydata - node.pos.y) < 0.5:
                    text = f"Node {node}: f({node.f}) = g({node.g}) + h({node.h})"
                    if self.clicked_signal:
                        self.clicked_signal.update_text.emit(text)
                    else:
                        print(text) 



    def init_graph_widget(self):
        """Plots the initial graph with default node colors"""
        self._ax = self.figure.add_subplot(111)
        self.figure.subplots_adjust(left=0.001, right=0.998, top=0.998, bottom=0.001)
        self.algorithm.plot_graph(self._ax)

        # Refresh the canvas
        self.canvas.draw()

    def update_graph_widget(self, full_run: bool = True) -> bool:
        """Clears the current graph and plots the current or the latest step.
        Args:
            full_run: bool: executes a full run of the algorithm or closes just the next node from the open list
        Returns:
            bool: True if target node is reached False otherwise
        """
        self.figure.clear()  # Clear the figure
        self._ax = self.figure.add_subplot(111)
        target_reached = False
        if full_run:
            target_reached = self.algorithm.full_run()
            self.algorithm.plot_graph(self._ax, show_current_node=True, show_closed=True, show_ideal_path=True)
        else:
            target_reached = self.algorithm.single_step_run()
            self.algorithm.plot_graph(self._ax, True, True, True, True)

        # Refresh the canvas
        self.canvas.draw()
        return target_reached
    
    def reset_graph(self):
        """Overwrites the current algorithm with a new one. Clears figure and draws new graph.
        """
        self.algorithm = A_star()
        self.figure.clear()
        self._ax = self.figure.add_subplot(111)
        self.algorithm.plot_graph(self._ax)
        self.canvas.draw()

class ConfigTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        v_layout = QVBoxLayout()
        # tab description
        v_layout.addWidget(QLabel('Initial Graph is loaded with algorithm from default values. Change values here and reload graph and algorithm parameters.'))
        # TODO: add config widgets
        self.setLayout(v_layout)