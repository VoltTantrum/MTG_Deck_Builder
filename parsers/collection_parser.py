import csv
class Collection_Parser():

    def __init__(self, source_file, source_name):
        self.source_file = source_file
        self.source_name = source_name

    def import_deck_list(self):
        my_deck_list = {}
        with open(self.source_file, "r") as csv_file:
            if self.source_name == "helvault":
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    name = row[3]
                    count = row[5]
                    set_name = row[-2]
                    my_deck_list[name] = count
        return my_deck_list
        