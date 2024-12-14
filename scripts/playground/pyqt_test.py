from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create a Matplotlib figure
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # Initialize the plot
        self.plot_sine_wave()

    def plot_sine_wave(self):
        """Plots a sine wave."""
        ax = self.figure.add_subplot(111)
        x = np.linspace(0, 2 * np.pi, 100)
        y = np.sin(x)
        ax.plot(x, y)
        ax.set_title("Sine Wave")
        ax.set_xlabel("x")
        ax.set_ylabel("sin(x)")

        # Refresh the canvas
        self.canvas.draw()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main window settings
        self.setWindowTitle("PyQt with Matplotlib")
        self.setGeometry(100, 100, 800, 600)

        # Create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Set up layout
        layout = QVBoxLayout(central_widget)

        # Add Matplotlib widget
        self.matplotlib_widget = MatplotlibWidget()
        layout.addWidget(self.matplotlib_widget)

        # Add a button to update the plot
        button = QPushButton("Update Plot")
        button.clicked.connect(self.update_plot)
        layout.addWidget(button)

    def update_plot(self):
        """Clears the current plot and adds a new random plot."""
        ax = self.matplotlib_widget.figure.clear()  # Clear the figure
        ax = self.matplotlib_widget.figure.add_subplot(111)
        x = np.linspace(0, 10, 100)
        y = np.random.rand(100)
        ax.plot(x, y, label="Random Data", color="orange")
        ax.legend()
        ax.set_title("Updated Plot")
        ax.set_xlabel("x")
        ax.set_ylabel("y")

        # Refresh the canvas
        self.matplotlib_widget.canvas.draw()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
