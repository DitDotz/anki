import sys
from PyQt5.QtCore import Qt  
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

    def init_ui(self):
        '''
        Initialises the main window of the Anki app.
        Has a create deck button along with buttons corresponding to existing deck names in the database
        '''
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
            deck_button.clicked.connect(lambda ch, name=deck_name: self.load_deck(name))  # Connect the button to a slot
            layout.addWidget(deck_button)

        self.setCentralWidget(central_widget)

    def get_deck_names_from_db(self): # working
        '''
        gets deck names necessary to instantiate deck_name buttons in the main window
        '''
        # Connect to the database and retrieve deck names
        conn = sqlite3.connect("flashcards.db")  # Replace with your database file
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM decks")
        deck_names = [row[0] for row in cursor.fetchall()]
        conn.close()
        return deck_names

    def show_create_deck_dialog(self): # working
        '''
        Pop-out dialogue window that allows user to input a custom deck name string
        '''
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
        '''
        Instantiate new deck in database using Deck class methods
        '''
        # Create a new instance of the Deck class with the entered deck name
        new_deck = main.Deck(deck_name)
        new_deck.save()  # Save the new deck to the database

        # Update the main menu with the new deck hyperlink
        self.update_main_menu(deck_name)

        # Close the dialog
        dialog.accept()

    def update_main_menu(self, deck_name): # working
        '''
        Create a hyperlink (QPushButton) for the new deck and add it to the main menu
        '''

        deck_button = QPushButton(deck_name)
        deck_button.clicked.connect(lambda ch, name=deck_name: self.load_deck(name))  # Connect the button to a slot
        self.centralWidget().layout().insertWidget(self.centralWidget().layout().count() - 1, deck_button)

    def load_deck(self, deck_name):
        '''
        Upon clicking a deck button, loads the deck behind the scenes, and open a separate window to review
        '''
        # Load the deck from the database using the load_deck class method
        selected_deck = main.Deck.load_deck(deck_name)

        # Open the review window with the selected Deck instance
        review_window = ReviewWindow(selected_deck, parent=self)
        review_window.show()

class ReviewWindow(QDialog): # Not working

    def __init__(self, deck, parent=None):
        super().__init__(parent)
        self.deck = deck
        # self.deck.get_cards_to_review()
        # self.deck.get_shuffled_cards()
        self.init_ui()

    def init_ui(self):
        # Have to break down Main.deck.review to get current questions and answers
        # get current_question
        # get current_answer

        self.setWindowTitle("Review Deck")
        self.setGeometry(100, 100, 400, 200)

        self.question_label = QLabel(str(self.deck.get_current_card().question)) # placeholder string returned by deck.review method
        self.question_label.setAlignment(Qt.AlignCenter)
        self.answer_label = QLabel('Placeholder')# Necessary placeholder
        self.answer_label.setAlignment(Qt.AlignCenter)
        self.answer_label.hide()

        self.show_answer_button = QPushButton("Show Answer")
        self.show_answer_button.clicked.connect(self.show_answer)

        # Create buttons for user response
        self.again_button = QPushButton("Again")
        self.hard_button = QPushButton("Hard")
        self.good_button = QPushButton("Good")
        self.easy_button = QPushButton("Easy")

        # Connect response buttons to corresponding actions
        self.again_button.clicked.connect(self.again)
        self.hard_button.clicked.connect(self.hard)
        self.good_button.clicked.connect(self.good)
        self.easy_button.clicked.connect(self.easy)

        # Initially hide the buttons
        self.again_button.hide()
        self.hard_button.hide()
        self.good_button.hide()
        self.easy_button.hide()

        #Set-up main menu layout
        layout = QVBoxLayout()
        layout.addWidget(self.question_label)
        layout.addWidget(self.answer_label)
        layout.addWidget(self.show_answer_button)

        # Use QHBoxLayout for horizontal alignment
        button_layout = QHBoxLayout()  
        button_layout.addWidget(self.again_button)
        button_layout.addWidget(self.hard_button)
        button_layout.addWidget(self.good_button)
        button_layout.addWidget(self.easy_button)
        # Add the horizontal button layout to main layout
        layout.addLayout(button_layout) 

        self.setLayout(layout)

    def show_answer(self):
        # Show the answer and hide the "Show Answer" button
        self.answer_label.setText(str(self.deck.get_current_card().answer)) # placeholder string returned by deck.review method
        self.answer_label.show()
        self.show_answer_button.hide()

        # Show the user response buttons
        self.again_button.show()
        self.hard_button.show()
        self.good_button.show()
        self.easy_button.show()


    # Have to change Deck.review implementation such that there is a dictionary
    # 'again': datetime
    # 'hard': datetime so on so forth

    # Define actions for user response buttons
    def again(self):
        # Handle the "Again" response here
        self.next_card()

    def hard(self):
        # Handle the "Hard" response here
        self.next_card()

    def good(self):
        # Handle the "Good" response here
        self.next_card()

    def easy(self):
        # Handle the "Easy" response here
        self.next_card()

    def next_card(self):
        # Move to the next card in the deck or close the window if there are no more cards
        self.deck.next_card()
        if self.deck.review():
            self.question_label.setText(self.deck.review().question)
            self.answer_label.clear()
        else:
            self.reject()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_menu = MainMenu()
    main_menu.show()
    sys.exit(app.exec_())
