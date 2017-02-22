
import random

def wait_for_player():
    '''()->None
    Pauses the program until the user presses enter
    '''
    try:
         input("\nPress enter to continue. ")
         print()
    except SyntaxError:
         pass


def make_deck():
    '''()->list of str
        Returns a list of strings representing the playing deck,
        with one queen missing.
    '''
    deck=[]
    suits = ['\u2660', '\u2661', '\u2662', '\u2663']
    ranks = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
    for suit in suits:
        for rank in ranks:
            deck.append(rank+suit)
    deck.remove('Q\u2663') # remove a queen as the game requires
    return deck

def shuffle_deck(deck):
    '''(list of str)->None
       Shuffles the given list of strings representing the playing deck    
    '''
    random.shuffle(deck)

def deal_cards(deck):
     '''(list of str)-> tuple of (list of str,list of str)

     Returns two lists representing two decks that are obtained
     after the dealer deals the cards from the given deck.
     The first list represents dealer's i.e. computer's deck
     and the second represents the other player's i.e user's list.
     '''
     
     dealer=[]
     other=[]
     while len(deck)>1:
          other.append(deck.pop())
          dealer.append(deck.pop())
     other.append(deck.pop()) # deal the last remaing card
     return (dealer, other)



def remove_pairs(l):
    '''
     (list of str)->list of str

     Returns a copy of list l where all the pairs from l are removed AND
     the elements of the new list shuffled

     Precondition: elements of l are cards represented as strings described above

     Testing:
     Note that for the individual calls below, the function should
     return the displayed list but not necessarily in the order given in the examples.

     >>> remove_pairs(['9♠', '5♠', 'K♢', 'A♣', 'K♣', 'K♡', '2♠', 'Q♠', 'K♠', 'Q♢', 'J♠', 'A♡', '4♣', '5♣', '7♡', 'A♠', '10♣', 'Q♡', '8♡', '9♢', '10♢', 'J♡', '10♡', 'J♣', '3♡'])
     ['10♣', '2♠', '3♡', '4♣', '7♡', '8♡', 'A♣', 'J♣', 'Q♢']
     >>> remove_pairs(['10♣', '2♣', '5♢', '6♣', '9♣', 'A♢', '10♢'])
     ['2♣', '5♢', '6♣', '9♣', 'A♢']
    '''

    no_pairs=[]

    l.sort()
    i=0
    while i<len(l)-1:
        card1=l[i]
        card2=l[i+1]
        if card1[0]==card2[0] and card1[1]==card2[1]: # if 10s need to compare first two chars
            i=i+1 # skip the next card
        elif card1[0]==card2[0]: # if not 10, it is enough to compare first chars
            i=i+1 # skip the next card
        else:
            no_pairs.append(l[i])
        i=i+1
    if i==len(l)-1: #this is true if the last card not a part of a pair
        no_pairs.append(l[i])

    random.shuffle(no_pairs)
    return no_pairs

def remove_pairs_v2(l):
    tmp=[]
    no_pairs=[]

    #create a list without suits
    for item in l:
        if len(item)==3: # corresponds to is rank '10'
            tmp.append(item[0]+item[1])
        else:
            tmp.append(item[0])

    #use it to determine which cards should stay 
    for i in range(len(tmp)):
        if tmp.count(tmp[i]) % 2==1 and i==tmp.index(tmp[i]):
            no_pairs.append(l[i])

 
    random.shuffle(no_pairs)
    return no_pairs


def print_deck(deck):
    '''
    (list)-None
    Prints elements of a given list deck separated by a space
    '''
    print()
    for item in deck:
        print(item, end=' ')
    print("\n")

def get_valid_input(n):
     '''
     (int)->int
     Returns an integer given by the user that is at least 1 and at most n.
     Keeps on asking for valid input as long as the user gives integer outside of the range [1,n]
     
     Precondition: n>=1
     '''
     print("I have", n, "cards. If 1 stands for my first card and")
     print(n, "for my last card, which of my cards would you like?")
     position=int(input("Give me an integer between 1 and "+str(n)+": ").strip())
     
     while not(position>=1 and position <=n):
          position=int(input("Invalid number. Please enter integer between 1 and "+str(n)+": ").strip())
     return position

def play_game():
     '''()->None
     This function plays the game'''
    
     deck=make_deck()
     shuffle_deck(deck)
     tmp=deal_cards(deck)
     dealer=tmp[0]
     human=tmp[1]

     print("Hello. My name is Robot and I am the dealer.")
     print("Welcome to my card game!")
     print("Your current deck of cards is:")
     print_deck(human)
     print("Do not worry. I cannot see the order of your cards")

     print("Now discard all the pairs from your deck. I will do the same.")
     wait_for_player()
     
     dealer=remove_pairs(dealer)
     human=remove_pairs(human)

     round_parity=0
     while len(dealer)>0 and len(human)>0:
          if round_parity==0: # dealer offers her cards
               print("***********************************************************")
               print("Your turn.")
               print("\nYour current deck of cards is:")
               print_deck(human)
               
               card_position=get_valid_input(len(dealer))
               item=dealer[card_position-1]
               dealer.remove(item) # this is valid since cards are unique

               # handled the four endings of ordinals in english
               english_ordinals_end=["st", "nd", "rd", "th"]
               if card_position>3:
                   ord_index=3
               else:
                   ord_index=card_position-1
                   
               print("You asked for my "+str(card_position)+english_ordinals_end[ord_index]+" card.")

               print("Here it is. It is", item)

               human.append(item)
               print("\nWith", item, "added, your current deck of cards is:")
               print_deck(human)

               print("And after discarding pairs and shuffling, your deck is:")
               human=remove_pairs(human)
               print_deck(human)

               wait_for_player()
               round_parity=1
          
          else:
               print("***********************************************************")
               print("My turn.\n")
               card_index=random.randint(0,len(human)-1)
               item=human[card_index]
               human.remove(item)
               dealer.append(item)
               dealer=remove_pairs(dealer)

               # handle the four endings of ordinals in English
               english_ordinals_end=["st", "nd", "rd", "th"]
               if card_index>2:
                   ord_index=3
               else:
                   ord_index=card_index

               print("I took your "+str(card_index+1)+english_ordinals_end[ord_index]+" card.")

               wait_for_player()
               round_parity=0
               
          
     if len(dealer)==0:
          print("Ups. I do not have any more cards")
          print("You lost! I, Robot, win")
     else:
          print("***********************************************************")
          print("Ups. You do not have any more cards")
          print("Congratulations! You, Human, win")
	
	 

play_game()
