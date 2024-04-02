import random, sys

# Definir las constantes.
HEARTS = chr(9829)  # Corazones
DIAMONDS = chr(9830)  # Diamantes
SPADES = chr(9824)  # Espadas
CLUBS = chr(9827)  # Tréboles
BACKSIDE = 'backside'  # Parte posterior de la carta, utilizada para ocultar la carta del dealer

def main():
    """Función principal que ejecuta el juego de Blackjack."""
    print(''' -- BLACKJACK --
    Rules:
        Try to get as close to 21 without going over.
        Kings, Queens, and Jacks are worth 10 points.
        Aces are worth 1 or 11 points.
        Cards 2 through 10 are worth their face value.
        (H)it to take another card.
        (S)tand to stop taking cards.
        On your first play, you can (D)ouble down to increase your bet
        but must hit exactly one more time before standing.
        If the dealer's visible card is an Ace, you can take insurance.
        In case of a tie, the bet is returned to the player.
        The dealer stops hitting at 17.''')

    money = 5000  # Dinero inicial del jugador
    while True:
        if money <= 0:
            print("You are broke! Good thing you weren't playing with real money.")
            print('Thanks for playing!')
            sys.exit()

        print('Money:', money)
        bet = getBet(money)  # Solicita al jugador hacer una apuesta

        deck = getDeck()  # Obtiene un mazo de cartas mezclado
        dealerHand = [deck.pop(), deck.pop()]  # Mano inicial del dealer
        playerHand = [deck.pop(), deck.pop()]  # Mano inicial del jugador

        insuranceBet = 0  # Inicializa la apuesta de seguro a 0
        if dealerHand[0][0] == 'A':
            insuranceBet = offerInsurance(bet)  # Ofrece seguro si la carta visible del dealer es un As

        print('Bet:', bet)
        while True:  # Ciclo de juego para el jugador
            displayHands(playerHand, dealerHand, False, insuranceBet > 0)
            print()

            if getHandValue(playerHand) > 21:
                break  # El jugador se pasa de 21

            move = getMove(playerHand, money - bet)  # Solicita al jugador su próximo movimiento

            if move == 'D':
                additionalBet = getBet(min(bet, (money - bet)))
                bet += additionalBet
                print(f'Bet increased to {bet}.')

            if move in ('H', 'D'):
                newCard = deck.pop()
                rank, suit = newCard
                print(f'You drew a {rank} of {suit}.')
                playerHand.append(newCard)

                if getHandValue(playerHand) > 21:
                    continue

            if move in ('S', 'D'):
                break

        handleDealerActions(dealerHand, deck)  # Acciones del dealer

        displayHands(playerHand, dealerHand, True, insuranceBet > 0)  # Muestra las manos finales

        playerValue = getHandValue(playerHand)
        dealerValue = getHandValue(dealerHand)
        moneyChange = handleBets(playerValue, dealerValue, bet, insuranceBet, dealerHand)  # Determina el resultado de la apuesta
        money += moneyChange
        print(f'Current Money: {money}')
        input('Press Enter to continue...')
        print('\n\n')

def getBet(maxBet):
    """Solicita al jugador que ingrese la cantidad de su apuesta."""
    while True:
        print(f'How much do you bet? (1-{maxBet}, or QUIT)')
        bet = input('> ').upper().strip()
        if bet == 'QUIT':
            print('Thanks for playing!')
            sys.exit()

        if not bet.isdecimal():
            continue

        bet = int(bet)
        if 1 <= bet <= maxBet:
            return bet

def getDeck():
    """Devuelve un mazo de cartas mezclado."""
    deck = []
    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2, 11):
            deck.append((str(rank), suit))
        for rank in ('J', 'Q', 'K', 'A'):
            deck.append((rank, suit))
    random.shuffle(deck)
    return deck

def displayHands(playerHand, dealerHand, showDealerHand, insurance=False):
    """Muestra las manos del jugador y del dealer."""
    print()
    if showDealerHand:
        print(f'DEALER: {getHandValue(dealerHand)}')
        displayCards(dealerHand)
    else:
        print('DEALER: ???')
        displayCards([BACKSIDE] + dealerHand[1:])

    print(f'PLAYER: {getHandValue(playerHand)}')
    displayCards(playerHand)
    if insurance:
        print("Insurance bet is active.")

def getHandValue(cards):
    """Calcula el valor de una mano de cartas."""
    value = 0
    numberOfAces = 0

    for card in cards:
        rank = card[0]
        if rank == 'A':
            numberOfAces += 1
        elif rank in ('K', 'Q', 'J'):
            value += 10
        else:
            value += int(rank)

    value += numberOfAces
    for i in range(numberOfAces):
        if value + 10 <= 21:
            value += 10

    return value

def displayCards(cards):
    """Muestra las cartas proporcionadas."""
    rows = ['', '', '', '', '']

    for i, card in enumerate(cards):
        rows[0] += ' ___  '
        if card == BACKSIDE:
            rows[1] += '|## | '
            rows[2] += '|###| '
            rows[3] += '|_##| '
        else:
            rank, suit = card
            rows[1] += f'|{rank.ljust(2)} | '
            rows[2] += f'| {suit} | '
            rows[3] += f'|_{rank.rjust(2, "_")}| '

    for row in rows:
        print(row)

def getMove(playerHand, money):
    """Solicita al jugador decidir su próximo movimiento."""
    while True:
        moves = ['(H)it', '(S)tand']

        if len(playerHand) == 2 and money > 0:
            moves.append('(D)ouble down')

        movePrompt = ', '.join(moves) + '> '
        move = input(movePrompt).upper()
        if move in ('H', 'S'):
            return move
        elif move == 'D' and '(D)ouble down' in moves:
            return move
        else:
            print("Invalid input. Please choose 'H', 'S', or 'D'.")

def offerInsurance(bet):
    """Ofrece la opción de seguro al jugador si la carta visible del dealer es un As."""
    while True:
        print("Dealer's up card is an Ace. Do you want to take insurance? (Y/N)")
        insurance = input('> ').upper().strip()
        if insurance == 'Y':
            insuranceBet = bet / 2
            print(f'Insurance bet of {insuranceBet} placed.')
            return insuranceBet
        elif insurance == 'N':
            return 0
        else:
            print("Please enter 'Y' for yes or 'N' for no.")

def handleDealerActions(dealerHand, deck):
    """Gestiona las acciones del dealer."""
    while getHandValue(dealerHand) < 17:
        print('Dealer hits...')
        dealerHand.append(deck.pop())
        if getHandValue(dealerHand) > 21:
            break
        input('Press Enter to continue...')
        print('\n\n')

def handleBets(playerValue, dealerValue, bet, insuranceBet, dealerHand):
    """Determina el resultado de la apuesta y devuelve el cambio en el dinero."""
    if playerValue > 21:
        print('You bust! You lost!')
        return -bet  # El jugador pierde la apuesta porque se pasó de 21
    elif dealerValue == 21 and len(dealerHand) == 2 and insuranceBet > 0:
        print('Dealer has Blackjack! Insurance bet wins.')
        return insuranceBet * 2
    elif dealerValue > 21:
        print(f'Dealer busts! You win ${bet}!')
        return bet
    elif playerValue > dealerValue:
        print(f'You win ${bet}!')
        return bet
    elif playerValue < dealerValue:
        print('Dealer wins! You lost!')
        return -bet
    else:
        print("It's a tie, the bet is returned to you.")
        return 0

if __name__ == '__main__':
    main()
