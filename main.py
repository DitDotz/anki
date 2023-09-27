import random
import datetime
import sqlite3


class Card:
    def __init__(
        self,
        question,
        answer,
        card_id=None,
        deck_id=None,
        interval=1,
        ease_factor=2.5,
        correct_attempts=0,
        due_date=None,
        last_review_date=None,
        review_attempts=0,
    ):
        self.card_id = card_id  # Instantiate after saving
        self.deck_id = deck_id  # Instantiate after saving
        self.question = question
        self.answer = answer
        self.interval = interval
        self.ease_factor = ease_factor
        self.correct_attempts = correct_attempts
        self.current_incorrect_attempts = 0
        self.due_date = datetime.date.today()  # Initial due date (today)
        self.last_review_date = last_review_date  # Last review date
        self.review_attempts = review_attempts  # Total review attempts

    def save(self):
        conn = sqlite3.connect("flashcards.db")
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO cards (question, answer, deck_id, interval, ease_factor, correct_attempts, due_date, last_review_date, review_attempts)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                self.question,
                self.answer,
                self.deck_id,
                self.interval,
                self.ease_factor,
                self.correct_attempts,
                self.due_date,
                self.last_review_date,
                self.review_attempts,
            ),
        )
        self.card_id = cursor.lastrowid  # Get the ID of the inserted deck
        conn.commit()
        conn.close()

    def edit_card(self, new_question, new_answer):  # Change to SQL implementation
        self.question = new_question
        self.answer = new_answer


class Deck:
    def __init__(self, name):
        self.name = name
        self.id = None  # The deck ID will be set after saving
        self.cards = []

    def add_card(self, card):
        card.deck_id = self.id
        self.cards.append(card)

    def remove_card(self, card):
        if card in self.cards:
            self.cards.remove(card)
        else:
            print("Card not found in the deck.")

    def save(self):
        conn = sqlite3.connect("flashcards.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO decks (name) VALUES (?)", (self.name,))
        self.id = cursor.lastrowid  # Get the ID of the inserted deck
        conn.commit()
        conn.close()

    def list_cards(self):
        for i, card in enumerate(self.cards, 1):
            print(f"Card {i} - Question: {card.question}, Answer: {card.answer}")

    def review(self):
        while self.cards:
            random.shuffle(self.cards)  # Shuffle the cards for review

            # Display current card
            card = self.cards[0]
            print(f"Question: {card.question}")
            user_response = input("Your answer: ").strip().lower()

            # Update card attributes
            card.review_attempts += 1  # Increment review attempts
            card.last_review_date = datetime.date.today()  # Update last review date

            # If correct
            if user_response == card.answer.strip().lower():
                print("Correct!")
                print(", ".join("%s: %s" % item for item in vars(card).items()))

                card.correct_attempts += 1

                card.interval *= (
                    card.ease_factor
                )  # Set the appropriate interval

                card.current_incorrect_attempts = (
                    0  # Reset incorrect attempts for next review
                )

                # Update card attribute
                card.due_date += datetime.timedelta(days=int(card.interval))

                # Update SQL database
                # Not working as intended - it is only taking the last card's attributes 
                conn = sqlite3.connect("flashcards.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE cards SET ease_factor = ?, interval = ?, correct_attempts = ?, due_date = ?, last_review_date = ?, review_attempts = ? WHERE id = ?", (card.ease_factor, card.interval, card.correct_attempts, card.due_date, card.last_review_date, card.review_attempts, card.card_id))
                conn.commit()
                conn.close()

                self.cards.pop(0)  # Remove the card from the review queue

            else:
                card.interval = 1  # Reset the interval for incorrect answers
                card.ease_factor -= 0.1  # Decrease the ease factor for every wrong attempt in current loop
                card.current_incorrect_attempts += 1
                self.cards.append(
                    self.cards.pop(0)
                )  # Move the card to the end of the queue
                print("Incorrect!")
                print(self.cards)

            card.interval = min(card.interval, 30)  # Apply maximum interval

        print(f"You have completed today's review")

    @classmethod
    def load_deck(cls, deck_id):
        conn = sqlite3.connect("flashcards.db")
        cursor = conn.cursor()

        # Execute the SQL query to select deck name
        cursor.execute("SELECT name FROM decks WHERE id = ?", (deck_id,))
        deck_name = cursor.fetchone()[0]

        # Create a new Deck instance with the fetched deck name
        deck = Deck(deck_name)

        # Execute the SQL query to select cards for the specified deck ID
        cursor.execute("SELECT * FROM cards WHERE deck_id = ?", (deck_id,))

        # Fetch all matching rows
        rows = cursor.fetchall()

        # Create Card objects for the fetched rows with card_id attribute
        cards = []
        for row in rows:
            card = Card(
                row[1], row[2], row[0], row[3]
            )  # card_id, question, answer, deck_id
            card.interval = row[4]
            card.ease_factor = row[5]
            card.correct_attempts = row[6]
            card.due_date = (
                datetime.datetime.strptime(row[7], "%Y-%m-%d").date() if row[7] else None
            )
            card.last_review_date = (
                datetime.datetime.strptime(row[7], "%Y-%m-%d").date() if row[8] else None
            )
            card.review_attempts = row[9]
            cards.append(card)
        conn.close()
        deck.cards = cards  # Store the loaded cards in the deck
        return deck


# # Create a deck
# my_deck = Deck("Test deck")
# my_deck.save()
# # Deck has to be created before adding cards to it.
# # Create cards
# card1 = Card("What is the capital of France?", "Paris")
# card2 = Card("What is your name?", "ZQ")
# # Add cards to deck
# my_deck.add_card(card1)
# my_deck.add_card(card2)
# # Save cards
# card1.save()
# card2.save()

deck = Deck.load_deck(1)
deck.review()
