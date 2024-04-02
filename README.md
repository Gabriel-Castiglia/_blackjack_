# _blackjack_ (Blackjack in Python)

This project is an extended version of the Blackjack game, based on the original code by Al Sweigart in his book "Invent Your Own Computer Games with Python". Additional features have been added to enrich the gameplay experience and offer more options to the player.

## Features

- **Basic Blackjack Gameplay**: The player attempts to get as close to 21 without going over, competing against a dealer who follows fixed rules for drawing cards.
- **Betting**: The player starts with an initial balance and places bets before each hand.
- **Double Down**: On their first turn, the player has the option to double their bet, but can only receive one more card afterward.
- **Insurance**: If the dealer's visible card is an Ace, the player can choose to take insurance, which is an additional bet that protects against the dealer having a blackjack.
- **Tie Handling**: In the event of a tie (push), the player's bet is returned.

## How to Play

1. Run `python3 blackjack.py` in your terminal to start the game.
2. Follow the on-screen instructions to place your bet, decide your move on each hand, and more.

## Enhancements over the Original Code

This project introduces several enhancements and additional features over Al Sweigart's basic version of Blackjack:

- **Insurance Implementation**: Allows the player to take insurance when the dealer's visible card is an Ace.
- **Double Down Feature**: Gives the player the option to double their bet with the chance of only receiving one more card.
- **User Input Validation**: Enhances the robustness of the game by ensuring all user inputs are valid before proceeding.
- **Improved Betting Handling**: Adjustments to the player's balance are made more clearly and consistently after each hand.

## Notes

This project is intended for educational purposes only and does not involve real money betting. It has been created as a way to learn and practice Python programming while exploring the development of simple terminal games.

## Acknowledgements

Thanks to Al Sweigart for his inspirational book "Invent Your Own Computer Games with Python", which served as the foundation for this project.

## License

This project is inspired by the work of Al Sweigart and is for educational purposes. It is available under the MIT License. See LICENSE file for more details.
