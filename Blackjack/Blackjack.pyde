import random

def setup():
    global bg, show_text, stageNum, welcome, picture, sum_of_dealer, sum_of_player
    global deck, player_hand, dealer_hand, card_images, game_state
    global hit_button, stand_button
    size(1500, 800)
    bg = loadImage("background.png")
    welcome = loadImage("welcome.jpg")
    show_text = True
    stageNum = 0
    sum_of_dealer= 0
    sum_of_player = 0
    deck = []
    player_hand = []
    dealer_hand = []
    card_images = {}
    game_state = "start"
    hit_button = {'x': 1200, 'y': 700, 'width': 100, 'height': 50, 'label': "Hit"}
    stand_button = {'x': 1350, 'y': 700, 'width': 100, 'height': 50, 'label': "Stand"}

    initialize_deck()
    shuffle_deck()
    start_game()
    


def draw():
    if stageNum == 0:
        drawWelcome() #welcome page
    elif stageNum == 1:
        drawinstructions()#instructions page
    elif stageNum == 2:
        drawGamePlay() #gameplay page

def drawinstructions():
    image(bg, 0, 0, width, height)
    fill(255)
    textSize(28)
    textAlign(LEFT, BASELINE)
    text("By drawing cards, try and achieve a hand as close to 21 as possible to beat the dealer!", 150, 100)
    text("Each number card associates with its corresponding point", 175, 150)
    text("Jack, Queen and King all correspond to 10 points", 200, 200)
    text("However, the Ace card can correspond to both 11 and 1", 225 , 250)
    text("However, be careful! Exceed 21, and the dealer wins", 250, 300)
    text("'Hit' to draw a card or 'Stand' to pass", 275, 350)
    text("Don't Forget!", 300, 400)

    if frameCount % 40 < 20: #to show the text periodically
        show_text = True
    else:
        show_text = False
    
    if show_text:
        fill(0 )
        text("Press any key to play....", 525, 600)
    stageNum = 1

def drawWelcome():
    image(welcome, 0, 0, width, height)
    fill(0)
    textSize(30)
    if frameCount % 40 < 20:
        show_text = True
    else:
        show_text = False
    
    if show_text:
        text("Press Spacebar to go next....", 525, 600)
    stageNum = 0

def keyPressed():
    global stageNum, game_state
    if (stageNum == 0) and (key == " "): # Welcome
        stageNum = 1 # Instructions
    elif (stageNum == 1):
        stageNum = 2 # Gameplay
    elif game_state == "game_over":
        if key == 'r' or key == 'R':  # Play again
            reset_game()
            stageNum = 1  # Go back to instructions
        elif key == 'n' or key == 'N':  # exit the game
            exit()

def initialize_deck():
    suits = ['hearts', 'diamonds', 'clubs', 'spades']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    for suit in suits:
        for value in values:
            deck.append(value + "of" + suit) #make a deck with the cards in it

def shuffle_deck():
    random.shuffle(deck) #randomize the deck

def start_game():
    global game_state
    for i in range(2):
        player_hand.append(deck.pop()) #give a card to the hand, it is popped because there is only one of the card in the deck
        dealer_hand.append(deck.pop())
    game_state = "player_turn"

def display_hand_player(x, y):
    global picture, sum_of_player
    offset = 0
    sum_of_player = 0
    number_of_aces = 0  # Track the number of aces

    for card in player_hand:
        picture = loadImage(card + '.png')
        image(picture, x + offset, y, 150, 200)
        card_score = get_card_score(card)
        sum_of_player += card_score
        if card_score == 11:  # Check if card is ace
            number_of_aces += 1 
        offset += 200

    # Decrease score by 10 if ace
    while sum_of_player > 21 and number_of_aces:
        sum_of_player -= 10
        number_of_aces -= 1

    fill(255)
    textSize(30)
    textAlign(LEFT, BASELINE)
    text("Current score is " + str(sum_of_player),50, 550 + 230)

def display_hand_dealer(x, y):
    global picture,sum_of_dealer
    offset = 0
    sum_of_dealer = 0
    number_of_aces = 0  # Count aces

    for card in dealer_hand:
        picture = loadImage(card + '.png')
        image(picture, x + offset, y, 150, 200)
        card_score = get_card_score(card)
        sum_of_dealer += card_score
        if card_score == 11:  # If the card is an ace
            number_of_aces += 1
        offset += 200


    while sum_of_dealer > 21 and number_of_aces:
        sum_of_dealer -= 10
        number_of_aces -= 1

    fill(255)
    textSize(30)
    textAlign(LEFT, BASELINE)
    text("Current score is " + str(sum_of_dealer), 600, 50 + 230) #display dealer score

def get_card_score(card):
    value = card.split("of")[0].strip() #remove the suit
    if value in ['J', 'Q', 'K']: #for letter cards
        return 10
    elif value == 'A':
        return 11
    else:
        return int(value) #for number cards

def calculate_hand_value(hand):
    value = 0 #track of hand score
    number_of_aces = 0
    for card in hand:
        rank = card.split('of')[0]
        if rank in ['J', 'Q', 'K']:
            value += 10
        elif rank == 'A':
            number_of_aces += 1
            value += 11
        else:
            value += int(rank)
    while value > 21 and number_of_aces: #if score is greater than 21 and there is ace score should be lower
        value -= 10
        number_of_aces -= 1
    return value

def draw_buttons():
    fill(0)
    rect(hit_button['x'], hit_button['y'], hit_button['width'], hit_button['height'])
    fill(255)
    text(hit_button['label'], hit_button['x'] + 20, hit_button['y'] + 35)
    
    fill(0)
    rect(stand_button['x'], stand_button['y'], stand_button['width'], stand_button['height'])
    fill(255)
    text(stand_button['label'], stand_button['x'] + 10, stand_button['y'] + 35)

def mousePressed():
    if (hit_button['x'] <= mouseX <= hit_button['x'] + hit_button['width'] and #collsion detection to check if button has been pressed
        hit_button['y'] <= mouseY <= hit_button['y'] + hit_button['height']):
        player_hit()
    elif (stand_button['x'] <= mouseX <= stand_button['x'] + stand_button['width'] and
          stand_button['y'] <= mouseY <= stand_button['y'] + stand_button['height']):
        player_stand()

def player_hit():
    global player_hand, deck, game_state
    if game_state == "player_turn": 
        player_hand.append(deck.pop()) #player gets another card
        if calculate_hand_value(player_hand) > 21:
            game_state = "game_over" #game moves to end stage if score is over 21

def drawGamePlay():
    global game_state
    image(bg, 0, 0, width, height)
    display_hand_player(50, 550)
    
    # Display only one card of the dealer if it's player's turn and stand button hasn't been pressed
    if game_state == "player_turn":
        display_hand_dealer_single_card(600, 50)
    else:
        display_hand_dealer(600, 50)
    
    
    draw_buttons()

    if game_state == "player_turn":
        sleeve = loadImage("sleeve.png")
        image(sleeve, 800, 50, 150, 200)
    elif game_state == "dealer_turn":
        dealer_turn()
    elif sum_of_player == 21 or sum_of_player > 21:
        check_winner()
        draw_game_over_options()
    elif game_state == "game_over":
        check_winner()
        draw_game_over_options()


def player_stand():
    global game_state
    if game_state == "player_turn":
        game_state = "dealer_turn"

def dealer_turn():
    global dealer_hand, deck, game_state
    while calculate_hand_value(dealer_hand) < 17:
        dealer_hand.append(deck.pop())
    game_state = "check_winner"
    check_winner()

def check_winner():
    global game_state
    if sum_of_player > 21: 
        game_state = "game_over"
        display_game_over_message("You busted! Dealer wins.")
    elif sum_of_dealer > 21:
        game_state = "game_over"
        display_game_over_message("Dealer busted! You win!")
    elif sum_of_player > sum_of_dealer:
        game_state = "game_over"
        display_game_over_message("You win with a higher hand!")
    elif sum_of_dealer > sum_of_player:
        game_state = "game_over"
        display_game_over_message("Dealer wins with a higher hand.")
    elif sum_of_player == sum_of_dealer:
        game_state = "game_over"
        display_game_over_message("It's a tie!")
    
def display_hand_dealer_single_card(x, y):
    global picture
    picture = loadImage(dealer_hand[0] + '.png')
    image(picture, x, y, 150, 200)
    sum = get_card_score(dealer_hand[0])
    
    # Adjust the score for Aces if needed
    if sum == 11 and calculate_hand_value(dealer_hand) > 21:
        sum = 1

    fill(255)
    textSize(30)
    text("Current score is " + str(sum), x , y + 230)
    
def display_game_over_message(message): #display the game end text based on the check winner function
    fill(255, 255, 255) 
    textSize(50)
    textAlign(CENTER, CENTER)
    text(message, width // 2, height // 2)
    


def draw_game_over_options():
    fill(255)
    textSize(30)
    textAlign(CENTER, CENTER)
    text("Press 'R' to play again", width // 2, height // 2 + 50)
    text("Press 'N' to exit", width // 2, height // 2 + 100)
    
def reset_game():
    global deck, player_hand, dealer_hand, game_state
    deck = []
    player_hand = [] #empty the hands
    dealer_hand = []
    game_state = "start"
    initialize_deck()
    shuffle_deck()
    start_game() 
