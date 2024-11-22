class Menu:
    def __init__(self, json):
        self.wc = json['wc']
        self.main = json['main']
        self.special = json['special']
        self.dessert = json['dessert']
        self.soup = json['soup']

    def __str__(self):
        msg = f"Menu for w/c {self.wc}:\n"
        for key in ['main', 'special', 'dessert', 'soup']:
            header = f"{key.capitalize()}:"
            msg += f"{header}\n" + "-" * len(header) + "\n"
            msg +=  f"{self.__dict__[key]}\n\n"
        return msg
