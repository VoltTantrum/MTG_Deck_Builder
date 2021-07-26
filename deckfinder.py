from parsers import collection_parser
from parsers import mtg_goldfish_parser
import operator


if __name__ == "__main__":
    my_coll_obj = collection_parser.Collection_Parser("helvault.csv", "helvault")
    my_coll = my_coll_obj.import_deck_list()
    goldfish_parser = mtg_goldfish_parser.Goldfish_Parser(my_coll)
    goldfish_parser.get_mtg_goldfish_deck_links()
    sorted_x = sorted(goldfish_parser.get_goldfish_decks(), key=operator.attrgetter('amount_owned'))
    [d.print_help() for d in sorted_x]
    