import sys

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QLabel,
    QLineEdit,
    QTextEdit,
)

import main

class AnkiUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Anki App')
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        # Create question input box
        self.question_label = QLabel('Question:') 
        self.layout.addWidget(self.question_label)
        self.question_edit = QTextEdit()
        self.layout.addWidget(self.question_edit)

        # Create answer input box
        self.answer_label = QLabel('Answer:')
        self.layout.addWidget(self.answer_label)
        self.answer_edit = QTextEdit()
        self.layout.addWidget(self.answer_edit)

        # Create button to create deck
        self.create_deck_button = QPushButton('Create deck')
        self.layout.addWidget(self.create_deck_button)

        # Create button to add flashcard to deck
        self.add_button = QPushButton('Add Flashcard')
        self.layout.addWidget(self.add_button)

        # Create button to review cards in deck
        self.review_button = QPushButton('Review Flashcards')

        # Initialize deck as None
        self.current_deck = None

        self.layout.addWidget(self.review_button)
        self.central_widget.setLayout(self.layout)
        self.create_deck_button.clicked.connect(self.create_deck)
        self.add_button.clicked.connect(self.add_flashcard)
        self.review_button.clicked.connect(self.review_flashcards)

 
    def create_deck(self):
        self.current_deck = main.Deck("Test deck")
        print('Deck created')

    def add_flashcard(self):
        if self.current_deck is not None:
            question = self.question_edit.toPlainText()
            answer = self.answer_edit.toPlainText()

            if question and answer:
                card = main.Flashcard(question, answer)
                self.current_deck.add_card(card)
                self.question_edit.clear()
                self.answer_edit.clear()
                print(f'Added flashcard: Question: {question}, Answer: {answer}' )
            else:
                    print("Please enter both question and answer before adding a flashcard.")
        else:
            print("Please create a deck before adding a flashcard.")

    def review_flashcards(self):
        if self.current_deck is not None:
            self.current_deck.review()
        else:
            print("Please select a deck before reviewing flashcards.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AnkiUI()
    window.show()
    sys.exit(app.exec_())
