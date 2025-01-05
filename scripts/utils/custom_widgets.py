from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGroupBox, QRadioButton, QDoubleSpinBox, QHBoxLayout, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, QObject
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.axes import Axes

from typing import Optional

from utils.a_start_algorithm import A_star, A_star_parameter
from utils.geometry import EuclidianDistance, ManhattenDistance

################
# Custom Signals
################

class TargetReachedSignal(QObject):
    reached = pyqtSignal(bool)

class ClickedSignal(QObject):
    # Define a custom signal
    update_text = pyqtSignal(str)

################
# Custom Widgets
################

class MatplotlibWidget(QWidget):
    """Widget for handling the matplotlib graph visualization. Calls the plot_graph function from the algorithm.

    Args:
        QWidget (_type_): parent widget
    """
    def __init__(self, parent=None, signal: Optional[QObject] = None, a_star_parameter: A_star_parameter = A_star_parameter()):
        super().__init__(parent)

        # create algorithm instance
        self.a_star_parameter = a_star_parameter
        self.algorithm = A_star(self.a_star_parameter)

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

        # add signal
        self.target_reached_signal = TargetReachedSignal()

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
    
    def reset_graph(self,):
        """Overwrites the current algorithm with a new one. Clears figure and draws new graph.
        """
        self.algorithm = A_star(self.a_star_parameter)
        self.figure.clear()
        self._ax = self.figure.add_subplot(111)
        self.algorithm.plot_graph(self._ax)
        self.canvas.draw()

class ConfigWidget(QWidget):
    def __init__(self, graph_widget: MatplotlibWidget, a_star_parameter: A_star_parameter = A_star_parameter(), parent=None):
        super().__init__(parent=parent)
        self.a_star_parameter = a_star_parameter

        self.setWindowTitle("A*-Algorithm settings")
        self.graph_widget:MatplotlibWidget = graph_widget

        v_layout = QVBoxLayout()
        # description
        v_layout.addWidget(QLabel('Initial Graph is loaded with algorithm from default parameters.\nChange values here and reload graph with new algorithm parameters.\n\n'))
        
        # distance functions
        group_box = QGroupBox("Select the method for calculating the distance:")
        group_box.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; }")
        group_layout = QVBoxLayout()
        self.euclidian_rb = QRadioButton(str(EuclidianDistance()))
        if self.a_star_parameter.distance_method == EuclidianDistance():
            self.euclidian_rb.setChecked(True)
        self.manhatten_rb = QRadioButton(str(ManhattenDistance()))
        if self.a_star_parameter.distance_method == ManhattenDistance():
            self.manhatten_rb.setChecked(True)
        group_layout.addWidget(self.euclidian_rb)
        group_layout.addWidget(self.manhatten_rb)
        group_box.setLayout(group_layout)
        v_layout.addWidget(group_box)

        # h scale
        h_scale_layout = QHBoxLayout()
        h_scale_layout.addWidget(QLabel('H scale factor: '))
        self.h_scale_sb = QDoubleSpinBox()
        self.h_scale_sb.setMinimum(-5.0)  # Set minimum value
        self.h_scale_sb.setMaximum(5.0)  # Set maximum value
        self.h_scale_sb.setSingleStep(0.1)  # Set the step size
        self.h_scale_sb.setDecimals(2)  # Number of decimal places
        self.h_scale_sb.setValue(self.a_star_parameter.h_scale)  # Set the initial value
        h_scale_layout.addWidget(self.h_scale_sb)
        v_layout.addLayout(h_scale_layout)

        # edge weights
        group_box = QGroupBox("Edge weights:")
        group_box.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; }")
        group_layout = QVBoxLayout()

        fixed_weight_layout = QHBoxLayout()
        self.fixed_edge_weight_rb = QRadioButton("Fixed weight: ")

        fixed_weight_layout.addWidget(self.fixed_edge_weight_rb)
        self.fixed_edge_weight_sb = QDoubleSpinBox()
        self.fixed_edge_weight_sb.setMinimum(0.1)
        self.fixed_edge_weight_sb.setMaximum(10)
        self.fixed_edge_weight_sb.setSingleStep(0.1)
        self.fixed_edge_weight_sb.setDecimals(1)
        if isinstance(self.a_star_parameter.edge_weight, float) or isinstance(self.a_star_parameter.edge_weight, int):
            self.fixed_edge_weight_rb.setChecked(True)
            self.fixed_edge_weight_sb.setValue(self.a_star_parameter.edge_weight)
        else:
            self.fixed_edge_weight_rb.setChecked(False)
        fixed_weight_layout.addWidget(self.fixed_edge_weight_sb)

        random_weight_layout = QHBoxLayout()
        self.random_edge_weight_rb = QRadioButton("Random weight: ")
        random_weight_layout.addWidget(self.random_edge_weight_rb)
        random_weight_layout.addWidget(QLabel('From: '))
        self.random_weight_sb_min = QDoubleSpinBox()
        self.random_weight_sb_min.setMinimum(1)
        self.random_weight_sb_min.setMaximum(10)
        self.random_weight_sb_min.setSingleStep(1)
        self.random_weight_sb_min.setDecimals(0)
        random_weight_layout.addWidget(self.random_weight_sb_min)
        random_weight_layout.addWidget(QLabel("To: "))
        self.random_weight_sb_max = QDoubleSpinBox()
        self.random_weight_sb_max.setMinimum(1)
        self.random_weight_sb_max.setMaximum(10)
        self.random_weight_sb_max.setSingleStep(1)
        self.random_weight_sb_max.setDecimals(0)
        if isinstance(self.a_star_parameter.edge_weight, tuple):
            self.random_edge_weight_rb.setChecked(True)
            self.random_weight_sb_min.setValue(self.a_star_parameter.edge_weight[0])
            self.random_weight_sb_max.setValue(self.a_star_parameter.edge_weight[1])
        else:
            self.random_edge_weight_rb.setChecked(False)
        random_weight_layout.addWidget(self.random_weight_sb_max)

        group_layout.addLayout(fixed_weight_layout)
        group_layout.addLayout(random_weight_layout)
        group_box.setLayout(group_layout)
        v_layout.addWidget(group_box)

        # choose start node
        start_node_layout = QHBoxLayout()
        start_node_layout.addWidget(QLabel('Startnode number: '))
        self.start_node_sb = QDoubleSpinBox()
        self.start_node_sb.setMinimum(1)  # Set minimum value
        self.start_node_sb.setMaximum(200)  # Set maximum value
        self.start_node_sb.setSingleStep(1)  # Set the step size
        self.start_node_sb.setDecimals(0)  # Number of decimal places
        self.start_node_sb.setValue(self.a_star_parameter.start_node)  # Set the initial value
        start_node_layout.addWidget(self.start_node_sb)
        v_layout.addLayout(start_node_layout)

        # choose target node
        target_node_layout = QHBoxLayout()
        target_node_layout.addWidget(QLabel('Targetnode number: '))
        self.target_node_sb = QDoubleSpinBox()
        self.target_node_sb.setMinimum(1)  # Set minimum value
        self.target_node_sb.setMaximum(200)  # Set maximum value
        self.target_node_sb.setSingleStep(1)  # Set the step size
        self.target_node_sb.setDecimals(0)  # Number of decimal places
        self.target_node_sb.setValue(self.a_star_parameter.target_node)  # Set the initial value
        target_node_layout.addWidget(self.target_node_sb)
        v_layout.addLayout(target_node_layout)

        # disabled nodes
        disabled_nodes_layout  = QHBoxLayout()
        disabled_nodes_layout.addWidget(QLabel('Disable nodes:'))
        self.disabled_nodes_input = QLineEdit()
        self.disabled_nodes_input.setPlaceholderText("ex.: 20, 21, 30-35")
        self.disabled_nodes_input.textChanged.connect(self.check_disabled_nodes_text)
        disabled_nodes_layout.addWidget(self.disabled_nodes_input)
        v_layout.addLayout(disabled_nodes_layout)
        self.disabled_nodes_error_label = QLabel()
        v_layout.addWidget(self.disabled_nodes_error_label)

        # Reload button
        reload_algo_button = QPushButton('Apply changes and reload')
        reload_algo_button.setIcon(QIcon("pictures/reload_button.jpg"))
        reload_algo_button.clicked.connect(self.reload_algo_and_plot)
        v_layout.addWidget(reload_algo_button)
        self.setLayout(v_layout)

    def check_disabled_nodes_text(self):
        check_ok = False
        if check_ok:
            self.disabled_nodes_error_label.setText("")
            self.disabled_nodes_error_label.hide()
        else:
            self.disabled_nodes_error_label.setText("Wrong text format for disabling nodes!")
            self.disabled_nodes_error_label.show()

    def reload_algo_and_plot(self):
        if self.euclidian_rb.isChecked():
            self.a_star_parameter.distance_method = EuclidianDistance()
        elif self.manhatten_rb.isChecked():
            self.a_star_parameter.distance_method = ManhattenDistance()
        self.a_star_parameter.h_scale = float(self.h_scale_sb.value())
        if self.fixed_edge_weight_rb.isChecked():
            self.a_star_parameter.edge_weight = float(self.fixed_edge_weight_sb.value())
        elif self.random_edge_weight_rb.isChecked():
            self.a_star_parameter.edge_weight = (int(self.random_weight_sb_min.value()), int(self.random_weight_sb_max.value()))
        self.a_star_parameter.start_node = int(self.start_node_sb.value())
        self.a_star_parameter.target_node = int(self.target_node_sb.value())

        self.graph_widget.reset_graph()
        self.close()
        self.graph_widget.target_reached_signal.reached.emit(False)


class DataWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        v_layout = QVBoxLayout()
        # tab description
        v_layout.addWidget(QLabel('Collection of graph data:'))
        v_layout.addWidget(QLabel('TODO...'))

        self.setLayout(v_layout)

class InfoPageWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Node color overview')
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('This shows information about the node coloring...'))
        self.setLayout(main_layout)

