import random


class Domino:
    
    def __init__(self):
        self.full_set = [[x, y] for x in range(7) for y in range(x, 7)]
        self.doubles = [[x, x] for x in range(7)]
        self.stock = self.player = self.comp = self.domino_snake = self.play_piece = []
        self.status = ''
    
    def shuffle(self):
        while True:
            random.shuffle(self.full_set)
            if any(x in self.doubles for x in self.full_set[14:]):
                break
        self.stock = self.full_set[:14]
        self.player = self.full_set[14:21]
        self.comp = self.full_set[21:]
    
    def snake(self):
        self.domino_snake = [max(x for x in self.doubles if x in self.full_set[14:])]
        if self.domino_snake[0] in self.comp:
            self.comp.remove(self.domino_snake[0])
            self.status = 'player'
        elif self.domino_snake[0] in self.player:
            self.player.remove(self.domino_snake[0])
            self.status = 'computer'
    
    def print(self):
        print(f"{'=' * 70}"
              f"\nStock size: {len(self.stock)}"
              f"\nComputer pieces: {len(self.comp)}\n")
        if len(self.domino_snake) < 7:
            print(*self.domino_snake, sep='')
        else:
            print(*self.domino_snake[:3], '...', *self.domino_snake[-3:], sep='')
        n = 0
        print("\nYour pieces:")
        while n < len(self.player):
            print(f"{n + 1}:{self.player[n]}")
            n += 1
    
    def check_input(self):
        while True:
            command = input()
            try:
                if abs(int(command)) > len(self.player):
                    raise IndexError
                return int(command)
            except (ValueError, IndexError):
                print("Invalid input. Please try again.")
    
    def turn(self):
        if self.status == "player":
            print("\nStatus: It's your turn to make a move. Enter your command.")
            counter = len(self.player)
            while True:
                piece = self.check_input()
                self.make_move(piece, self.player)
                if counter != len(self.player):
                    break
                print("Illegal move. Please try again")
            self.status = "computer"
        
        elif self.status == "computer":
            print("\nStatus: Computer is about to make a move. Press Enter to continue...")
            if input() == "":
                scores = self.calculate_score(self.domino_snake, self.comp)
                counter = len(self.comp)
                while True:
                    if len(scores) == 0:
                        self.make_move(0, self.comp)
                        break
                        
                    piece = max(scores, key=scores.get)
                    self.make_move(piece, self.comp)
                    if counter != len(self.comp):
                        break
                    
                    piece = -piece
                    self.make_move(piece, self.comp)
                    if counter != len(self.comp):
                        break

                    del scores[abs(piece)]
                    
                self.status = "player"
    
    def make_move(self, index, hands):
        if index == 0:
            hands.append(self.stock.pop())
        else:
            play_piece = hands[abs(index) - 1]
            if index > 0:
                try:
                    if self.domino_snake[-1][-1] in play_piece:
                        self.play_piece = play_piece
                        if self.domino_snake[-1][-1] == self.play_piece[0]:
                            self.domino_snake.append(self.play_piece)
                        else:
                            self.domino_snake.append(self.play_piece[::-1])
                        hands.remove(self.play_piece)
                    else:
                        raise TypeError
                except TypeError:
                    pass
            elif index < 0:
                try:
                    if self.domino_snake[0][0] in play_piece:
                        self.play_piece = play_piece
                        if self.domino_snake[0][0] == play_piece[0]:
                            self.domino_snake.insert(0, self.play_piece[::-1])
                        else:
                            self.domino_snake.insert(0, self.play_piece)
                        hands.remove(self.play_piece)
                    else:
                        raise TypeError
                except TypeError:
                    pass
                
    @staticmethod
    def calculate_score(snake, hand):
        number = {key: [] for key in range(7)}
        count_list = snake.copy()
        count_list.extend(hand)
        available_num = [i for x in count_list for i in x]
    
        for i, x in enumerate(available_num):
            number[x].append(i)
        count = {key: len(value) for (key, value) in number.items()}
        indexes = {key: 0 for key in range(1, len(hand) + 1)}
        n = 0
        for key, value in indexes.items():
            indexes[key] = count[hand[n][0]] + count[hand[n][1]]
            n += 1
        return indexes
    

def main():
    game = Domino()
    game.shuffle()
    game.snake()
    game.print()
    while True:
        game.turn()
        game.print()
        if len(game.player) == 0:
            print("\nStatus: The game is over. You won!")
            break
        elif len(game.comp) == 0:
            print("\nStatus: The game is over. The computer won!")
            break
        elif len(game.stock) == 0:
            print("\nStatus: The game is over. It's a draw!")
            break


if __name__ == "__main__":
    main()
