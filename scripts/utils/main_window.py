# standard lib
from typing import Optional

# Third-party imports
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QLabel, QSizePolicy
from PyQt5.QtCore import pyqtSignal, QObject
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.axes import Axes

# Local application imports
from utils.a_start_algorithm import A_star

class TargetReachedSignal(QObject):
    reached = pyqtSignal(bool)

class ClickedSignal(QObject):
    # Define a custom signal
    update_text = pyqtSignal(str)

class MatplotlibWidget(QWidget):
    """Widget for handling the matplotlib graph visualization. Calls the plot_graph function from the algorithm.

    Args:
        QWidget (_type_): parent widget
    """
    def __init__(self, parent=None, signal: Optional[ClickedSignal] = None):
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


class MainWindow(QMainWindow):
    """Main Layout of the applikation"""

    def __init__(self):
        super().__init__()

        # Main window settings
        self.setWindowTitle("A* PyQt and Matplotlib")
        self.setGeometry(50, 50, 1800, 1000)

        # Create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Set up layout
        layout = QVBoxLayout(central_widget)

        # Add Matplotlib widget
        self.clicked_signal = ClickedSignal()
        self.matplotlib_widget = MatplotlibWidget(signal=self.clicked_signal)
        layout.addWidget(self.matplotlib_widget)

        # Add buttons to update the plot
        button_layout = QHBoxLayout()
        button_next = QPushButton("Next step")
        button_next.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        button_next.clicked.connect(lambda: self.button_algorithm_action(False))
        button_layout.addWidget(button_next)
        

        button_last = QPushButton("Complete run")
        button_last.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        button_last.clicked.connect(lambda: self.button_algorithm_action(True))
        
        self.target_reached_signal = TargetReachedSignal()
        self.target_reached_signal.reached.connect(lambda hide: self.hide_buttons(hide, button_next, button_last))
        button_layout.addWidget(button_last)

        # Add Label to give node information
        label_node_info = QLabel("")
        label_node_info.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.clicked_signal.update_text.connect(label_node_info.setText)
        button_layout.addWidget(label_node_info)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(0)

        layout.addLayout(button_layout)

    def hide_buttons(self, hide: bool, button_next: QPushButton, button_last: QPushButton):
        if hide:
            button_next.setDisabled(hide)
            button_last.setDisabled(hide)
            

    def button_algorithm_action(self, full_run = False):
        target_reached = self.matplotlib_widget.update_graph_widget(full_run)
        if target_reached:
            self.target_reached_signal.reached.emit(True)





if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
