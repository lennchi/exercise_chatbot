from PyQt6.QtWidgets import QMainWindow, QPushButton, QApplication, QTextEdit, QLabel
from PyQt6.QtGui import QIcon, QKeyEvent
from PyQt6.QtCore import Qt
import sys
from backend import Chatbot, api_key
from config import gpt_model
import threading


class ChatbotWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.chatbot = Chatbot(api_key)

        self.setMinimumSize(600, 440)
        self.setWindowTitle("Jendy The Exercise Chatbot")  # Set window title
        self.setWindowIcon(QIcon('img/dumbbell_icon.png'))  # Set window icon
        self.setStyleSheet("background-color: white; ")  # Set background

        # Chat area
        self.chat_area = QTextEdit(self)
        self.chat_area.setGeometry(10, 10, 600, 320)  # Set position and size
        self.chat_area.setReadOnly(True)  # Prevent user from placing the cursor in the chat area
        self.chat_area.setStyleSheet("""
            QTextEdit {
            border: none; 
            padding: 10px 50px 10px 20px;
            }
        """)

        # GPT model label
        self.model_label = QLabel(self)
        self.model_label.setGeometry(450, 320, 200, 20)  # Set position and size
        self.model_label.setText(f"powered by {gpt_model}")
        self.model_label.setStyleSheet("""
                    QLabel {
                    color: #999999;
                    font-size: 10px;
                    }
                    """)

        # Input field
        self.input_field = QTextEdit(self)
        self.input_field.setGeometry(10, 340, 570, 60)  # Set position and size
        self.input_field.setStyleSheet("""
            QTextEdit {
            background-color: #e7e7e7;
            padding: 10px 60px 10px 20px;
            font-size: 14px;
            border: none;
            border-radius: 30px
            }
            """)

        # Send button
        self.button = QPushButton(self)
        self.button.setGeometry(530, 340, 60, 60)  # Set position and size
        self.button.setIcon(QIcon('img/send_circle_icon_gray_bg_44.png'))  # Set send icon
        self.button.setIconSize(self.button.size())  # Set icon size to button size
        self.button.setStyleSheet("""
            QPushButton {
            background-color: #e7e7e7;
            border: none;
            border-radius: 30px
            }
        """)

        self.button.clicked.connect(self.send_msg)

        self.show()

    def send_msg(self):
        user_input = self.input_field.toPlainText().strip()

        if user_input:
            # Append the user input to the chat area
            self.chat_area.append(f"<p style='color: #777777; font-size: 14px; '>⚪ <b>Me</b>: {user_input} \n</p>")
            # Clear the input field
            self.input_field.clear()

            # Start a new thread to get the bot response
            thread = threading.Thread(target=self.get_bot_response, args=(user_input,))
            thread.start()

    def get_bot_response(self, user_input):
        response = self.chatbot.get_response(user_input)
        # Add the bot response to the chat area
        self.chat_area.append(f"<p style='color: #333333; font-size: 14px; '>⚫ <b>Jendy</b>: {response} \n</p>")

    def keyPressEvent(self, event: QKeyEvent):
        # Check if the key pressed is Enter without Shift
        if event.key() == Qt.Key.Key_Return and not event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
            self.send_msg()
            event.accept()
        else:
            # Call the base class method for other keys
            super().keyPressEvent(event)


app = QApplication(sys.argv)
main_window = ChatbotWindow()
sys.exit(app.exec())