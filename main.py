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

        # Update the card's information in the SQLite database
        conn = sqlite3.connect("flashcards.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE cards SET question = ?, answer = ? WHERE id = ?", (new_question, new_answer, self.card_id))
        conn.commit()
        conn.close()

    def delete_card(self):
        # Delete the card entry from the SQLite database
        conn = sqlite3.connect("flashcards.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cards WHERE id = ?", (self.card_id,))
        conn.commit()
        conn.close()

    def update_interval(self, quality):
        '''
        Simplified SM2 algorithm.
        Possible improvements
        - 
        '''
        if quality == 'again':
            self.interval = 1  # Reset interval
        elif quality == 'hard':
            self.interval = max(self.interval * 1.2, 1)  # Increase interval, but not less than 1 day
        elif quality == 'good':
            self.interval *= min(self.ease_factor,14)  # Increase interval based on ease factor
        elif quality == 'easy':
            self.interval *= min(self.ease_factor * 2,30)  # Increase interval even more for 'easy'

class Deck:
    def __init__(self, name):
        self.name = name
        self.id = None  # The deck ID will be set after saving
        self.cards = []

    def add_card(self, card):
        '''
        Updates the card.deck_id attribute to be linked with current Deck instance
        '''
        card.deck_id = self.id
        self.cards.append(card)

        # Update the card's deck_id in the SQLite database
        conn = sqlite3.connect("flashcards.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE cards SET deck_id = ? WHERE id = ?", (card.deck_id, card.card_id))
        conn.commit()
        conn.close()

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

    # def get_cards_to_review(self):
    #     # Need to implement setting up today's cards for review
    #     # A mix of new and old cards
    #     return(cards_to_review)

    def get_shuffled_cards(self):
        shuffled_cards = random.shuffle(self.cards)  # Shuffle the cards for review
        return(shuffled_cards)

    def get_current_card(self):
        current_card = self.cards[0]
        return(current_card)
    
    def clear_current_card(self):
        self.cards.pop(0)  # Remove the card from the review queue
        return()        

    def get_cards_for_review(self):
        '''
        Selects both difficult cards to re-review and new cards to review
        Should be a option that the user can edit in the future
        '''
        max_new_cards = 10
        max_mature_cards = 10

        new_cards = []
        mature_cards = []

        for card in self.cards:
            if card.interval == 1 and len(new_cards) < max_new_cards:
                new_cards.append(card)

            elif card.due_date == datetime.date.today() and len(mature_cards) < max_mature_cards:
                mature_cards.append(card)

            if len(new_cards) >= 10 and len(mature_cards) >= 10:
                break
        
        cards_for_review = new_cards + mature_cards

        return cards_for_review


    def review2(self):
        '''
        Updated review to work with UI
        '''
        # Cards are shuffled automatically upon pressing ReviewWindow


    def review(self):
        # For testing
        # re-do this, get rid of the while loop, and print statements
        # Read through the implementation of the logic below
        # https://docs.ankiweb.net/deck-options.html


        # self.get_cards_to_review()
        self.get_shuffled_cards()

        while self.cards:
            # Display current card
            card = self.get_current_card()
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

                self.clear_current_card()
                
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
    def load_deck(cls, deck_name):
        conn = sqlite3.connect("flashcards.db")
        cursor = conn.cursor()

        # Execute the SQL query to select deck name
        cursor.execute("SELECT id FROM decks WHERE name = ?", (deck_name,))
        deck_id = cursor.fetchone()[0]

        # Create a new Deck instance with the fetched deck name
        deck = Deck(deck_name)

        deck.id = deck_id

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
                datetime.datetime.strptime(row[8], "%Y-%m-%d").date() if row[8] else None
            )
            card.review_attempts = row[9]
            cards.append(card)
        conn.close()
        deck.cards = cards  # Store the loaded cards in the deck
        return deck

#Area for unit testing
# Need to check if get_cards_for_review is working


# Create dummy cards to test get_cards_for_review
# Not sure why deck_id is not updating properly

# Reset flashcards.db as necessary using git restore

deck = Deck.load_deck('Test deck')

cards = []
for i in range(3, 33):
    question = f"Question {i}"
    answer = f"Answer {i}"
    card = Card(question, answer)
    card.save()
    deck.add_card(card)

