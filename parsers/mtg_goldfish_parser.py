from typing import Collection
from bs4 import BeautifulSoup
import requests
import re
from .deck import Deck

from threading import Thread

class Goldfish_Parser():

    def __init__(self, my_collection):
        self.decks = []
        self.my_coll = my_collection

    def get_mtg_goldfish_deck_links(self):
        page = requests.get("https://www.mtggoldfish.com/metagame/standard/full#paper")
        soup = BeautifulSoup(page.text, 'html.parser')
        threads = []
        for chunk in soup.find_all(class_='archetype-tile'):
            thread = Thread(target=self.get_single_deck, args=(chunk,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        threads = []
        for deck in self.decks:
            thread = Thread(target=deck.check_owned_cards, args=(self.my_coll,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        
        self.remove_dup_decks()
    
    def get_single_deck(self, chunk):
        curr_deck = chunk.find('a')
        statistics = chunk.find(class_='archetype-tile-statistic-value').text
        deck_name = curr_deck.find(class_="sr-only").text
        meta_percentage_unformated = statistics if "%" in statistics else "N/A"
        meta_percentage = meta_percentage_unformated.strip('\n').split('\n')[0]
        deck_link = curr_deck.get("href")
        if not "/archetype/standard-other-eld" in deck_link:
            deck_cards = self.get_mtg_goldfish_deck_cards(deck_link)
            new_deck = Deck(meta_percentage, deck_name, deck_cards)
            self.decks.append(new_deck)
            new_deck.check_owned_cards(self.my_coll)

    
    def get_mtg_goldfish_deck_cards(self, deck_link):
        cards = {}
        if "archetype" in deck_link:
            page = requests.get('https://www.mtggoldfish.com/'+ str(deck_link))
            soup = BeautifulSoup(page.text, 'html.parser')
            blob = soup.find('a', text = re.compile(r'^Text File \(Default\)$'), attrs = {'class' : 'dropdown-item'})
            deck_link = blob.get("href")
        if not "download" in deck_link:
            lnk = deck_link.split("/", 3)
            deck_link = "/"+lnk[1]+"/download/"+lnk[2]

        txt_of_deck = requests.get("https://www.mtggoldfish.com"+str(deck_link)).text
        for card in txt_of_deck.split("\r"):
            if not card.isspace():
                lst = card.split(" ", 1)
                card_name = lst[1]
                card_count = lst[0].split("\n")[1] if "\n" in lst[0] else lst[0]
                cards[card_name] = card_count 
        return cards
    
    def remove_dup_decks(self):
        pruned_decks = []
        seen_decks = []
        for deck in self.decks:
            if deck.name not in seen_decks:
                pruned_decks.append(deck)
                seen_decks.append(deck.name)
        return pruned_decks
    
    def get_goldfish_decks(self):
        return self.decks