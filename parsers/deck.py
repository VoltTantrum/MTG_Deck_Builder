class Deck():
    def __init__(self, meta_per, name, cards):
        self.meta_percentage = meta_per
        self.cards = cards
        self.name = name
        self.owned_cards = {}
        self.amount_owned = 0
    
    def print_help(self):
        print("\n -------------------------")
        print(self.name)
        print("\nCard list:")
        for card in self.cards:
            print(card + " - "+self.cards[card], end=", ")
        print("\n\n")
        print("Owned cards - " + str(len(self.owned_cards))+ ":")
        for card in self.owned_cards:
            print(card + " - "+self.owned_cards[card], end=", ")
        print()
        

    def check_owned_cards(self, my_card_list):
        for own_card in my_card_list:
            if own_card in self.cards:
                self.owned_cards[own_card] = my_card_list[own_card]
                self.amount_owned += 1
            