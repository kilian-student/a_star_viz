# standard lib

# Third-party imports
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QLabel, QSizePolicy, QTabWidget, QAction
from PyQt5.QtGui import QIcon

# Local application imports
from utils.custom_widgets import MatplotlibWidget, ConfigWidget, DataWidget, InfoPageWidget, TargetReachedSignal, ClickedSignal
from utils.a_start_algorithm import A_star_parameter


class MainWindow(QMainWindow):
    """Main Layout of the application"""

    def __init__(self):
        super().__init__()

        # Main window settings
        self.setWindowTitle("A* PyQt and Matplotlib")
        self.setGeometry(50, 50, 1800, 1000)

        # Create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        ##########
        # Menu bar
        ##########
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu(QIcon('pictures/settings_button.png'), "File")
        info_menu = menu_bar.addMenu("Info")

        # Add "Info" action
        info_action = QAction("Node colors", self)
        info_action.triggered.connect(self.show_info_page)
        info_menu.addAction(info_action)

        # Add "Settings" action
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.show_config_page)
        file_menu.addAction(settings_action)

        ###############
        # Window Layout
        ###############
        layout = QVBoxLayout(central_widget)

        # Tab widget
        tab_widget = QTabWidget()

        # Add Matplotlib widget to tabwidget
        self.clicked_signal = ClickedSignal()
        self.a_star_parameter = A_star_parameter()
        self.matplotlib_widget = MatplotlibWidget(signal=self.clicked_signal, a_star_parameter=self.a_star_parameter)
        tab_widget.addTab(self.matplotlib_widget, "Graph")

        # Add Config Tab widget to tabwidget
        self.config_widget = DataWidget(self)
        tab_widget.addTab(self.config_widget, "Data")

        layout.addWidget(tab_widget, 0)

        # Add buttons to update the plot
        button_layout = QHBoxLayout()
        button_next = QPushButton("Next step")
        button_next.setIcon(QIcon("pictures/play_button.png"))
        button_next.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        button_next.clicked.connect(lambda: self.button_algorithm_action(False))
        button_layout.addWidget(button_next)
        

        button_last = QPushButton("Complete run")
        button_last.setIcon(QIcon("pictures/next_button.png"))
        button_last.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        button_last.clicked.connect(lambda: self.button_algorithm_action(True))
        button_layout.addWidget(button_last)
        
        self.matplotlib_widget.target_reached_signal.reached.connect(lambda hide: self.hide_buttons(hide, button_next, button_last))
        
        button_reset = QPushButton("Reset graph")
        button_reset.setIcon(QIcon("pictures/reload_button.jpg"))
        button_reset.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        button_reset.clicked.connect(self.reset_graph_action)
        button_layout.addWidget(button_reset)

        # Add Label with clicked node information
        label_node_info = QLabel("")
        label_node_info.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.clicked_signal.update_text.connect(label_node_info.setText)
        button_layout.addWidget(label_node_info)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(0)

        layout.addLayout(button_layout)

    def show_info_page(self):
        self.info_widget = InfoPageWidget()
        self.info_widget.show()

    def show_config_page(self):
        self.config_widget = ConfigWidget(self.matplotlib_widget, self.a_star_parameter)
        self.config_widget.show()

    def hide_buttons(self, hide: bool, button_next: QPushButton, button_last: QPushButton):
        button_next.setDisabled(hide)
        button_last.setDisabled(hide)

    def reset_graph_action(self):
        self.matplotlib_widget.reset_graph()
        self.matplotlib_widget.target_reached_signal.reached.emit(False)
            
    def button_algorithm_action(self, full_run = False):
        target_reached = self.matplotlib_widget.update_graph_widget(full_run)
        if target_reached:
            self.matplotlib_widget.target_reached_signal.reached.emit(True)





if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
