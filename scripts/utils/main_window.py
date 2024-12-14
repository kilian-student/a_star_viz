# Third-party imports
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Local application imports
from utils.a_start_algorithm import A_star

class MatplotlibWidget(QWidget):
    """Widget for handling the matplotlib graph visualization. Calls the plot_graph function from the algorithm.

    Args:
        QWidget (_type_): parent widget
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        # create algorithm instance
        self.algorithm = A_star()

        # Create a Matplotlib figure
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # Initialize the plot
        self.init_graph_widget()

    def init_graph_widget(self):
        """Plots the initial graph with default node colors"""
        ax = self.figure.add_subplot(111)
        self.figure.subplots_adjust(left=0.001, right=0.998, top=0.998, bottom=0.001)
        self.algorithm.plot_graph(ax)

        # Refresh the canvas
        self.canvas.draw()

    def update_graph_widget(self, full_run: bool = True):
        """Clears the current graph and plots the current or the latest step.
        Args:
            full_run: bool: executes a full run of the algorithm or closes just the next node from the open list
        """
        ax = self.figure.clear()  # Clear the figure
        ax = self.figure.add_subplot(111)
        if full_run:
            self.algorithm.full_run()
            self.algorithm.plot_graph(ax, show_closed=True)
        else:
            self.algorithm.single_step_run()
            self.algorithm.plot_graph(ax, True, True, True)

        # Refresh the canvas
        self.canvas.draw()


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
        self.matplotlib_widget = MatplotlibWidget()
        layout.addWidget(self.matplotlib_widget)

        # Add a button to update the plot
        button_layout = QHBoxLayout()
        button_next = QPushButton("Next step")
        button_next.clicked.connect(lambda: self.matplotlib_widget.update_graph_widget(False))
        button_layout.addWidget(button_next)

        button_last = QPushButton("Complete run")
        button_last.clicked.connect(lambda: self.matplotlib_widget.update_graph_widget(True))
        button_layout.addWidget(button_last)

        layout.addLayout(button_layout)



if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
