import os
from PyQt5 import QtWidgets, QtGui, QtCore
import txt  # Assuming you have this module with text content
import qdarkstyle

class MultiLayerQuestionsApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multi-Layer Questions")
        self.setGeometry(100, 100, 900, 1080)
        self.trend_context = None
        self.history_stack = []
        self.current_layer = 0
        self.trend_context_map = {
            'BTC': 1,
            'TOTAL3': 2,
            'BTC.D': 3,
            'Uptrend': 1,
            'Downtrend': 2,
            'Ranges': 3,
            'Chop': 4
        }
        self.init_ui()  # Call the init_ui method here

    def init_ui(self):  # Make sure this method is indented properly
        layout = QtWidgets.QVBoxLayout(self)

        # Scroll Area to hold content
        scroll_area = QtWidgets.QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_content = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout(scroll_content)
        scroll_area.setWidget(scroll_content)

        # Layer, Question, Options, Result labels and frames
        self.layer_label = QtWidgets.QLabel("Current Layer: 0")
        self.layer_label.setFont(QtGui.QFont("Arial", 9))
        self.layer_label.setAlignment(QtCore.Qt.AlignLeft)
        self.layer_label.setContentsMargins(20, 10, 20, 0)  # Adjust margins as needed
        self.scroll_layout.addWidget(self.layer_label)

        self.question_label = QtWidgets.QLabel("Start the quiz")
        self.question_label.setFont(QtGui.QFont("Arial", 16))
        self.question_label.setAlignment(QtCore.Qt.AlignLeft)
        self.question_label.setContentsMargins(20, 5, 20, 0)  # Adjust margins as needed
        self.scroll_layout.addWidget(self.question_label)

        # Option layout (for buttons)
        self.option_layout = QtWidgets.QHBoxLayout()
        self.option_layout.setContentsMargins(20, 5, 20, 0)  # Adjust margins as needed
        self.scroll_layout.addLayout(self.option_layout)

        self.result_label = QtWidgets.QLabel("")
        self.result_label.setFont(QtGui.QFont("Arial", 14))
        self.result_label.setWordWrap(True)
        self.result_label.setAlignment(QtCore.Qt.AlignLeft)
        self.result_label.setContentsMargins(20, 10, 20, 0)  # Adjust margins as needed
        self.scroll_layout.addWidget(self.result_label)

        # Create a horizontal layout for the image
        image_layout = QtWidgets.QHBoxLayout()
        image_layout.setContentsMargins(0, 0, 0, 0)  # No margins for the image layout

        # Image label with 20px margins on left and right, 0px on top and bottom
        self.image_label = QtWidgets.QLabel("")
        self.image_label.setContentsMargins(0, 0, 0, 0)  # No margins for the image itself
        self.image_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        image_layout.addWidget(self.image_label)
        self.scroll_layout.addLayout(image_layout)

        layout.addWidget(scroll_area)

        # Reset and Exit buttons
        button_layout = QtWidgets.QHBoxLayout()
        reset_button = QtWidgets.QPushButton("Reset/Clear")
        reset_button.clicked.connect(self.go_back)
        button_layout.addWidget(reset_button)

        exit_button = QtWidgets.QPushButton("Exit")
        exit_button.clicked.connect(QtWidgets.qApp.quit)
        button_layout.addWidget(exit_button)

        button_layout.setContentsMargins(20, 5, 20, 5)  # Adjust margins as needed
        layout.addLayout(button_layout)

        # Initialize first layer
        self.handle_answer(0, txt.x, [1, 2, 3], self.process_layer)

    def handle_answer(self, layer, question_text, options, answer_callback):
        self.current_layer = layer
        self.layer_label.setText(f"Current Layer: {layer}")
        self.question_label.setText(question_text)

        # Clear previous options
        for i in reversed(range(self.option_layout.count())):
            widget = self.option_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Add option buttons
        for idx, opt in enumerate(options):
            btn = QtWidgets.QPushButton(str(opt))
            btn.setFont(QtGui.QFont("Arial", 17))
            btn.clicked.connect(lambda checked, opt=opt: answer_callback(layer, opt))
            self.option_layout.addWidget(btn)

    def go_back(self):
        if self.current_layer > 0:
            self.current_layer -= 1
            self.result_label.setText("")
            self.image_label.clear()
            if self.current_layer == 0:
                self.handle_answer(0, txt.x, [1, 2, 3], self.process_layer)
            else:
                self.process_layer(self.current_layer, self.trend_context_map[self.trend_context])

    def process_layer(self, layer, answer):
        if layer == 0:
            if answer == 1:  # BTC
                self.trend_context = None
                self.handle_answer(1, txt.xx, [1, 2, 3, 4], self.process_layer_btc)
            elif answer == 2:  # TOTAL3
                self.trend_context = None
                self.handle_answer(1, txt.xx, [1, 2, 3, 4], self.process_layer_total3)
            elif answer == 3:  # BTC.D
                self.trend_context = None
                self.handle_answer(1, txt.xx_d, [1, 2, 3], self.process_layer_btcd)

    def process_layer_btc(self, layer, answer):
        if layer == 1:
            if answer == 1:
                self.trend_context = 'Uptrend'
                self.handle_answer(2, txt.a, [1, 2, 3, 4], self.process_layer_btc)
            elif answer == 2:
                self.trend_context = 'Downtrend'
                self.handle_answer(2, txt.ba, [1, 2, 3, 4, 5], self.process_layer_btc)
            elif answer == 3:
                self.trend_context = 'Ranges'
                self.handle_answer(2, txt.ca, [1, 2, 3], self.process_layer_btc)
            elif answer == 4:
                self.trend_context = 'Chop'
                self.display_text(txt.da, None)
        elif layer == 2:
            if self.trend_context == 'Uptrend':
                if answer == 1:
                    self.display_text(txt.aaa, "aaa.png")
                elif answer == 2:
                    self.display_text(txt.aab, "aab.png")
                elif answer == 3:
                    self.display_text(txt.aac, "aac.png")
                elif answer == 4:
                    self.display_text(txt.aae, "aae.png")
            elif self.trend_context == 'Downtrend':
                if answer == 1:
                    self.display_text(txt.baa, "baa.png")
                elif answer == 2:
                    self.display_text(txt.bab, "bab.png")
                elif answer == 3:
                    self.display_text(txt.bac, "bac.png")
                elif answer == 4:
                    self.display_text(txt.bad, "bad.png")
                elif answer == 5:
                    self.display_text(txt.bae, "bae.png")
            elif self.trend_context == 'Ranges':
                if answer == 1:
                    self.display_text(txt.caa, "caa.png")
                elif answer == 2:
                    self.display_text(txt.cab, "cab.png")
                elif answer == 3:
                    self.display_text(txt.cac, "cac.png")

    def process_layer_total3(self, layer, answer):
        if layer == 1:
            if answer == 1:
                self.trend_context = 'Uptrend'
                self.handle_answer(2, txt.a, [1, 2, 3, 4], self.process_layer_total3)
            elif answer == 2:
                self.trend_context = 'Downtrend'
                self.handle_answer(2, txt.ba, [1, 2, 3, 4, 5], self.process_layer_total3)
            elif answer == 3:
                self.trend_context = 'Ranges'
                self.handle_answer(2, txt.ca, [1, 2, 3], self.process_layer_total3)
            elif answer == 4:
                self.trend_context = 'Chop'
                self.display_text(txt.da, None)
        elif layer == 2:
            if self.trend_context == 'Uptrend':
                if answer == 1:
                    self.display_text(txt.aaa_1, "aaa_1.png")
                elif answer == 2:
                    self.display_text(txt.aab_1, "aab_1.png")
                elif answer == 3:
                    self.display_text(txt.aac_1, "aac_1.png")
                elif answer == 4:
                    self.display_text(txt.aad_1, "aad_1.png")
            elif self.trend_context == 'Downtrend':
                if answer == 1:
                    self.display_text(txt.baa_1, "baa_1.png")
                elif answer == 2:
                    self.display_text(txt.bab_1, "bab_1.png")
                elif answer == 3:
                    self.display_text(txt.bac_1, "bac_1.png")
                elif answer == 4:
                    self.display_text(txt.bad_1, "bad_1.png")
                elif answer == 5:
                    self.display_text(txt.bae_1, "bae_1.png")
            elif self.trend_context == 'Ranges':
                if answer == 1:
                    self.display_text(txt.caa_1, "caa_1.png")
                elif answer == 2:
                    self.display_text(txt.cab_1, "cab_1.png")
                elif answer == 3:
                    self.display_text(txt.cac_1, "cac_1.png")

    def process_layer_btcd(self, layer, answer):
        if layer == 1:
            if answer == 1:
                self.trend_context = 'Uptrend'
                self.display_text(txt.aaa_2, "aaa_2.png")
            elif answer == 2:
                self.trend_context = 'Downtrend'
                self.display_text(txt.baa_2, "baa_2.png")
            elif answer == 3:
                self.trend_context = 'Ranges'
                self.display_text(txt.caa_2, "caa_2.png")
    
    def display_text(self, text, image_name):
        self.result_label.setText(text)

        if image_name:
            base_dir = os.path.abspath(os.path.dirname(__file__))
            image_path = os.path.join(base_dir, "Pictures", image_name)

            if os.path.exists(image_path):
                pixmap = QtGui.QPixmap(image_path)

                # Set the maximum size based on the image label's size
                max_width = self.image_label.width()  # Use image label width
                max_height = self.image_label.height()  # Use image label height
                self.image_label.setMaximumSize(max_width, max_height)

                # Scale the image to fit within the image label's size, keeping aspect ratio
                scaled_pixmap = pixmap.scaled(self.image_label.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                self.image_label.setPixmap(scaled_pixmap)
            else:
                QtWidgets.QMessageBox.critical(self, "Error", f"Image '{image_name}' not found at '{image_path}'")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    # Apply the QDarkStyle theme here
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    window = MultiLayerQuestionsApp()
    window.show()
    app.exec_()
