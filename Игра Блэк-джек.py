# Блэк - Джэк
# От 1 до 7 игроков против дилера
import cards, games

class BJ_Card(cards.Card): #Расширяет функционал базового класса
    """ Карта для игры в Блек-джек."""
    ACE_VALUE = 1 # Ценность туза == 1
    @property
    
    def value(self): # Возвращает число из диапозона от 1 до 10 / Стоимость карты
        if self.is_face_up: # Если карта открыта
            v = BJ_Card.RANKS.index(self.rank) + 1 #Берёт атрибут rank (её истинный номинал) и находит порядковый номер этого номинала в BJ_Card.RANKS 
            if v > 10: # Для валета, дамы и короля эта велечина больше 10, присваиваем 10
                v = 10
        else: # Если is_face_up будет равно False(карта закрыта), возвращаем значение None
                v = None
        return v


class BJ_Deck(cards.Deck): # Предназначен для создания колоды карт, почти полностью совпадает с базовым классом cards.Deck
    """Колода для игры в Блек-джек."""
    
    def populate(self):
        for suit in BJ_Card.SUITS:
            for rank in BJ_Card.RANKS:
                self.cards.append(BJ_Card(rank, suit)) # А вот тут отличие, калода наполняется картами класса BJ_Card
                
    def check_lot(self):
        if len(self.cards) < 32:
            self.cards = []
            self.populate()
            self.shuffle()
            print("Перетасованная карта включает сброс")
            
            
class BJ_Hand(cards.Hand):
    """'Рука': набор карт "Блек-джека" у одного игрока."""
    
    def __init__(self, name):
        super(BJ_Hand, self).__init__()
        self.name = name # Добавляем атрибут name, представляющий имя игрока
        
    def __str__(self): # Переопределяем метод так, что теперь он отображает сумму очков на руках у игрока
        rep = self.name + ":\t" + super(BJ_Hand, self).__str__()
        if self.total:
            rep += "(" + str(self.total) + ")"
        return rep
    
    @property # Свойство, переделывает функцию в атрибут, для её вызова нет необходимости вызывать скобки
    def total(self): # Подсчёт стоимости карт
        #Если у одной из карт value равно None, то и всё свойство равно None
        for card in self.cards: #Перебирает карты игрока, список Player
            if not card.value: # Если карта закрыта
                return 0 # Возвращаем стоимость 0
        # Суммируем очки, считая каждый туз за 1 очко
        t = 0
        for card in self.cards:
            t += card.value # Конкатенация(склеивание) ценности карт
        # Определяем есть ли туз на руках у игрока
        contains_ace = False # Проверка на туза
        for card in self.cards:
            if card.value == BJ_Card.ACE_VALUE: # Разобрать логику работы с тузом
                contains_ace = True # Если туз в колоде, True
        # Если на руках есть туз и сумма очков не превышает 11, будем считать туз за 11 очков
        if contains_ace and t <= 11: # Если есть туз и общий пул очков меньше или равно 11
            # Прибавляем только 10, потому что 1 вошла в общую сумму
            t += 10
        return t
    
    def is_busted(self): # Возвращает True, когда свойство total объект принимает значение больше 21
        return self.total > 21 # Возвращаю логическое значение истинности в return

class BJ_Player(BJ_Hand): # Экземплярами класса BJ_Player, производного от BJ_Hand являются игроки
    """ Игрок в "Блек-джек"."""
    
    def is_hitting(self):
        response = games.ask_yes_no("\n" + self.name + ", будете брать ещё карты? (Y/N): ")
        return response == "y" # Возвращает True или False в зависимости от ввода игрока
    
    def bust(self):
        print(self.name, "перебрал")
        self.lose()
    
    def lose(self):
        print(self.name, "проиграл")
        print()
    
    def win(self):
        print(self.name, "выйграл.")
        print()
    
    def push(self):
        print(self.name, "сыграл с компьютеров в ничью")


class BJ_Dealer(BJ_Hand): # Является дилер игры
    """ Дилер в игре "Блек-джек"""
   
    def is_hitting(self): # Определяет, будет ли диллер брать доп карту
        return self.total < 17
   
    def bust(self): # Определяет, что дилер перебрал
        print(self.name, "перебрал.")
   
    def flip_first_card(self): # Переворачивает первую карту дилера лицевой стороной вниз
        first_card = self.cards[0]
        first_card.flip()


class BJ_Game(object):
    """Игра в "Блек-джек"."""
   
    def __init__(self, names): # Принимает список имён и создаёт на каждое имя по игроку
        self.players = []
        self.dealer = BJ_Dealer("Диллер")
        for name in names:
            player = BJ_Player(name)
            self.players.append(player)
        self.dealer = BJ_Dealer("Dealer")
        self.deck = BJ_Deck()
        self.deck.populate()
        self.deck.shuffle()
        self.bankrupt = 0
        self.shutdown = 0
    
    @property
    def still_playing(self): # Свойство still_playing возвращает список всех игроков, которые ещё остались в игре.
        sp = []
        for player in self.players:
            if not player.is_busted():
                sp.append(player)
        return sp
   
    def __additional_cards(self, player): # Сдаёт игроку или дилеру доп карты пока объект is_busted Возвращает False
        # а метод is_hitting() возвращает True
        while not player.is_busted() and player.is_hitting(): # ПОЛИМОРФИЗМ! метод is_hitting сработает вне зависимости от ого, к какому классу
            # относится объект player
            self.deck.deal([player]) # Метод deal делает перебор списка, а так как player это не часть списка без заключения player в квадратные скобки - будет ошибка
            # deck это атрибут класса BJ_Game, которая взял в себя класс BJ_Deck у которого есть метод deal
            print(player) # Выводит представление класса Player, его карты
            if player.is_busted(): #!!! Если стоимость карт выше 21: ( проверить каким образом Player имеет значение value?)
                player.bust() # Сообщение о переборе

    
    def play(self): # Основной цикл игры, схож с псевдокодом. 
        # Сдача всем по 2 карты
        self.deck.deal(self.players + [self.dealer], per_hand = 2) # Игроки, включая диллера получают по 2 карты
        self.dealer.flip_first_card() # Первая из карт у дилера переворачивается рубашкой вверх
        for player in self.players: #Перебор списка с игроками
            print(player)#Выводится экземпляры классов через метод __str__(Из списка игроков)
        print(self.dealer)#Выводится экземпляры классов через метод __str__
        # Сдача доп карт игрокам
        for player in self.players:#Перебор списка игроков
            self.__additional_cards(player)#Обращение к методу Game для добора карт 
        self.dealer.flip_first_card() # Первая карта дилера раскрывается
        if not self.still_playing:#Проверяет списки игроков, если игроки есть
            # Все игроки перебрали, покажем тольк "руку" дилера
            print(self.dealer)#Выводит статы диллера
        else: 
            # сдача доп карт дилеру
            print(self.dealer)#Выводит свои статы
            self.__additional_cards(self.dealer)#Добавляет карты дилеру пока не выше 17
            if self.dealer.is_busted():#Если привысил 21
                # Выйгрывают все, кто остался в игре
                for player in self.still_playing:#Перебирает список игркоов
                    player.win()# Объявляет их победителями
            else:
                # Сравниваем суммы очков у дилера и у игроков, оставшихся в игре
                for player in self.still_playing:
                    if player.total > self.dealer.total:
                        player.win()
                    elif player.total < self.dealer.total:
                        player.lose()
                    else:
                        player.push()
        # Удаление всех карт
        for player in self.players:
            player.clear()
        self.dealer.clear()
        self.deck.check_lot()#Проверка на количество и пересбор новой колоды
        
       
def main():
    print("Добро пожаловать за игровой стол Блек-джека!\n")
    names = []
    number = games.ask_number("Сколько всего игркоов? (1 - 7): ", low = 1, high = 8)
    for i in range(number):
        name = input("Введите имя игрока: ")
        names.append(name)
        print()
    game = BJ_Game(names)
    again = None
    while again != "n":
        game.play()
        again = games.ask_yes_no("\nХотите сыграть ещё раз? ")
    input("\n\nНажмите Enter, чтобы выйти.")
main()
input("\n\nНажмите Enter, чтобы выйти.")
        

    
