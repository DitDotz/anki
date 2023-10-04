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
    QDialog,
    QHBoxLayout
)

import main

import sqlite3

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    # Working as intended
    def init_ui(self):
        self.setWindowTitle("Flashcard App")

        # Create a central widget and layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        # Create a "Create Deck" button
        create_deck_button = QPushButton("Create Deck")
        create_deck_button.clicked.connect(self.show_create_deck_dialog)  # Connect the button to the create_deck method
        layout.addWidget(create_deck_button)

        # Create deck titles as hyperlinks (QPushButtons)
        deck_names = self.get_deck_names_from_db()

        for deck_name in deck_names:
            deck_button = QPushButton(deck_name)
            deck_button.clicked.connect(lambda ch, name=deck_name: self.start_review(name))  # Connect the button to a slot
            layout.addWidget(deck_button)

        self.setCentralWidget(central_widget)

    def get_deck_names_from_db(self): # working
        # Connect to the database and retrieve deck names
        conn = sqlite3.connect("flashcards.db")  # Replace with your database file
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM decks")
        deck_names = [row[0] for row in cursor.fetchall()]
        conn.close()
        return deck_names

    def show_create_deck_dialog(self): # working
        dialog = QDialog(self)
        dialog.setWindowTitle("Create Deck")
        dialog.setGeometry(100, 100, 300, 100)

        # Create a layout for the dialog
        layout = QVBoxLayout()

        # Create a label and input field for entering the deck name
        label = QLabel("Deck Name:")
        input_field = QLineEdit()

        # Create a layout for the input field and button
        input_layout = QHBoxLayout()
        input_layout.addWidget(label)
        input_layout.addWidget(input_field)

        # Create a button to confirm deck creation
        create_button = QPushButton("Create")
        create_button.clicked.connect(lambda: self.create_deck(input_field.text(), dialog))  # Connect the button to create_deck

        layout.addLayout(input_layout)
        layout.addWidget(create_button)
        dialog.setLayout(layout)

        dialog.exec_()

    def create_deck(self, deck_name, dialog): # working 
        # Create a new instance of the Deck class with the entered deck name
        new_deck = main.Deck(deck_name)
        new_deck.save()  # Save the new deck to the database

        # Update the main menu with the new deck hyperlink
        self.update_main_menu(deck_name)

        # Close the dialog
        dialog.accept()

    def update_main_menu(self, deck_name): # working
        # Create a hyperlink (QPushButton) for the new deck and add it to the main menu
        deck_button = QPushButton(deck_name)
        deck_button.clicked.connect(lambda ch, name=deck_name: self.start_review(name))  # Connect the button to a slot
        self.centralWidget().layout().insertWidget(self.centralWidget().layout().count() - 1, deck_button)

    def start_review(self, deck_id):
        # Load the deck from the database using the load_deck class method
        selected_deck = main.Deck.load_deck(deck_id)

        # Open the review window with the selected Deck instance
        review_window = ReviewWindow(selected_deck)
        review_window.show()

class ReviewWindow(QWidget): # Not working

    def __init__(self, deck_name):
        super().__init__()
        self.deck = deck
        self.current_question_index = 0
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"Review - {self.deck.name}")

        # Load questions from the database based on the deck name
        self.load_questions_from_db()

        # Create labels for the question and answer
        self.question_label = QLabel(self.questions[self.current_question_index]["question"])
        self.answer_label = QLabel("")
        self.answer_label.hide()

        # 'Add card to deck' button
        add_card_button = QPushButton('Add Card')

        # 'Show hidden answer' button
        show_answer_button = QPushButton("Show Answer")

        # 'Ease of recall' buttons
        # Upon pressing show answer, display 4 buttons - again, hard, good, easy
        # Upon pressing one of these 4 buttons, go next question
        again_button = QPushButton("Again") # < 1m
        hard_button = QPushButton("Hard") # < 6m
        good_button = QPushButton("Good") # < 10m
        easy_button = QPushButton("Easy") # 3d

        # Need to alter the review button to fit t
        show_answer_button.clicked.connect(self.show_answer)
        again_button.clicked.connect(Deck.review(param = 'again')) # alter this
        again_button.clicked.connect(Deck.review(param = 'hard')) # alter this
        again_button.clicked.connect(Deck.review(param = 'good')) # alter this
        again_button.clicked.connect(Deck.review(param = 'easy')) # alter this

        # Create a layout for the window
        layout = QVBoxLayout()
        layout.addWidget(self.question_label)
        layout.addWidget(self.answer_label)
        layout.addWidget(show_answer_button)
        layout.addWidget(next_question_button)

        self.setLayout(layout)

    def load_questions_from_db(self):
        # Implement logic to load questions from the database based on the deck name
        conn = sqlite3.connect("flashcards.db")  # Replace with your database file
        cursor = conn.cursor()
        cursor.execute("SELECT question, answer FROM cards WHERE deck_name = ?", (self.deck_name,))
        self.questions = [{"question": row[0], "answer": row[1]} for row in cursor.fetchall()]
        conn.close()

    def show_answer(self):
        # Show the answer when the button is clicked
        self.answer_label.setText(self.questions[self.current_question_index]["answer"])
        self.answer_label.show()

    def next_question(self):
        # Move to the next question
        self.current_question_index += 1

        # Check if there are more questions to display
        if self.current_question_index < len(self.questions):
            self.question_label.setText(self.questions[self.current_question_index]["question"])
            self.answer_label.setText("")
            self.answer_label.hide()

        else:
            self.question_label.setText("No more questions in this deck.")
            self.answer_label.setText("")
            self.answer_label.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_menu = MainMenu()
    main_menu.show()
    sys.exit(app.exec_())
