import random
import datetime

class Card:
    card_counter = 1  # Class-level counter for generating unique card IDs

    def __init__(self, question, answer, interval=1, ease_factor=2.5):
        self.card_id = Card.card_counter  # Unique identifier for the card

        self.question = question
        self.answer = answer
        self.deck_name = None  # Initialize deck_name as None
        self.interval = interval
        self.ease_factor = ease_factor
        self.correct_attempts = 0
        self.current_incorrect_attempts = 0
        self.due_date = datetime.date.today()  # Initial due date (today)
        self.last_review_date = None  # Last review date
        self.review_attempts = 0  # Total review attempts
        Card.card_counter +=1

    def edit_card(self, new_question, new_answer):
        self.question = new_question
        self.answer = new_answer

class Deck:
    deck_counter = 1 # Class-level counter for generating unique deck IDs

    def __init__(self, name=None):
        self.name = name
        self.cards = []
        self.deck_id = Deck.deck_counter
        Deck.deck_counter += 1  # Increment the deck ID counter

    def add_card(self, card):
        card.deck_name = self.name  # Set the deck_name attribute in the Card class
        self.cards.append(card)

    def remove_card(self, card):
        if card in self.cards:
            self.cards.remove(card)
        else:
            print("Card not found in the deck.")

    def list_cards(self):
        for i, card in enumerate(self.cards, 1):
            print(f"Card {i} - Question: {card.question}, Answer: {card.answer}")

    def review(self):
        while self.cards:
            random.shuffle(self.cards)  # Shuffle the cards for review

            card = self.cards[0]

            print(f"Question: {card.question}")
            user_response = input("Your answer: ").strip().lower()
            card.review_attempts += 1  # Increment review attempts
            card.last_review_date = datetime.date.today()  # Update last review date

            if user_response == card.answer.strip().lower():

                if card.current_incorrect_attempts >= 1:
                    card.correct_attempts += 1
                    card.interval *= (
                        card.ease_factor
                    )  # Decrease the interval for incorrect answers
                    self.cards.pop(0)  # Remove the card from the review queue
                    card.current_incorrect_attempts = (
                        0  # Reset incorrect attempts for next review
                    )
                    card.due_date += datetime.timedelta(days=int(card.interval))
                    print("Correct!")
                    print(', '.join("%s: %s" % item for item in vars(card).items()))

                else:
                    card.correct_attempts += 1
                    card.interval *= (
                        card.ease_factor
                    )  # Increase the interval for correct answers
                    self.cards.pop(0)  # Remove the card from the review queue
                    card.due_date += datetime.timedelta(days=int(card.interval))
            
                    print("Correct!")
                    print(', '.join("%s: %s" % item for item in vars(card).items()))

            else:
                card.interval = 1  # Reset the interval for incorrect answers
                card.ease_factor -= 0.1
                card.current_incorrect_attempts += 1
                self.cards.append(
                    self.cards.pop(0)
                )  # Move the card to the end of the queue
                print("Incorrect!")
                print(f"New interval: {card.interval:.1f} days\n")
                print(self.cards)

            card.interval = min(card.interval, 30)  # Apply maximum interval

        print(f"You have completed today's review")


# Create cards
card1 = Card("What is the capital of France?", "Paris")
card2 = Card("What is your name?", "ZQ")

# Create a deck
my_deck = Deck("Test deck")

# Add cards to deck
my_deck.add_card(card1)
my_deck.add_card(card2)

# Review deck
my_deck.review()
