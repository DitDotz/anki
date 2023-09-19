import random


class Flashcard:
    def __init__(
        self, question, answer, interval=1, ease_factor=2.5, incorrect_attempts=0
    ):
        self.question = question
        self.answer = answer
        self.interval = interval
        self.ease_factor = ease_factor
        self.incorrect_attempts = incorrect_attempts


class Deck:
    def __init__(self, name):
        self.name = name
        self.cards = []

    def add_card(self, card):
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
            user_response = input("Your answer: ").strip()

            if user_response == card.answer.strip().lower():
                if card.incorrect_attempts >= 1:
                    card.ease_factor -= 0.1
                    card.interval *= (
                        card.ease_factor
                    )  # Decrease the interval for incorrect answers
                    self.cards.pop(0)  # Remove the card from the review queue
                    card.incorrect_attempts = (
                        0  # Reset incorrect attempts for next review
                    )
                    print("Correct!")
                    print(f"New interval: {card.interval:.1f} days\n")

                else:
                    card.interval *= (
                        card.ease_factor
                    )  # Increase the interval for correct answers
                    self.cards.pop(0)  # Remove the card from the review queue
                    print("Correct!")
                    print(f"New interval: {card.interval:.1f} days\n")

            else:
                card.interval = 1  # Reset the interval for incorrect answers
                card.incorrect_attempts += 1
                self.cards.append(
                    self.cards.pop(0)
                )  # Move the card to the end of the queue
                print("Incorrect!")
                print(f"New interval: {card.interval:.1f} days\n")
                print(self.cards)

            card.interval = min(card.interval, 30)  # Apply maximum interval

        print(f"You have completed today's review")


# Create cards
card1 = Flashcard("What is the capital of France?", "Paris")
card2 = Flashcard("What is your name?", "ZQ")

# Create a deck
my_deck = Deck("Test deck")

# Add cards to deck
my_deck.add_card(card1)
my_deck.add_card(card2)

# Review deck
my_deck.review()
