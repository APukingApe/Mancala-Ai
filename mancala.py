import argparse
import sys
from time import time
import multiprocessing
import random

from io import StringIO

DEPTH = 2
DONT_SCORE_ONE = True
MANCALA = 6
CHESS = 4
node_counter = 0
setup = 10e1000
f=open("count.txt", "a+")



def compute(x):
    move_sequence, board = x
    return [x + 1 for x in move_sequence], board.mini_max_alpha_beta(DEPTH)
    #return [x + 1 for x in move_sequence], board.lucky(DEPTH)

class Board:
    PLAYER_SCORE_HOLDER = MANCALA + 1
    def __str__(self, *args, **kwargs):
        return str(self.board)

    def __repr__(self, *args, **kwargs):
        return "Board%s" % self.__str__()

    @property
    def player_points(self):
        if self.no_more_moves():
            return sum(self.board[1:self.PLAYER_SCORE_HOLDER + 1])
        else:
            return self.board[self.PLAYER_SCORE_HOLDER]

    @property
    def opponent_points(self):
        if self.no_more_moves():
            return self.board[0] + sum(self.board[self.PLAYER_SCORE_HOLDER + 1:])
        else:
            return self.board[0]

    def __init__(self, board=None):
        self.board = []
        # self.node_counter = 0

        if board is not None:
            self.board = board.board[:]
            self.reversed = board.reversed
        else:
            j = 0
            while j < 2:
                i = 0
                self.board.append(0)
                while i < MANCALA:
                    self.board.append(CHESS)
                    i = i + 1
                j = j + 1
            # self.board = [0, 4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4]
            self.reversed = False

    def make_player_move(self, n):
        assert n < MANCALA
        n += 1
        tokens = self.board[n]
        assert tokens > 0
        self.board[n] = 0
        while tokens:
            tokens -= 1
            n += 1
            if n >= len(self.board):
                n = 1
            self.board[n] += 1

        if n == self.PLAYER_SCORE_HOLDER:
            return True

        if self.board[n] == 1 and 0 < n < self.PLAYER_SCORE_HOLDER:
            oponent_pos = len(self.board) - n
            if DONT_SCORE_ONE is False or (DONT_SCORE_ONE is True and self.board[oponent_pos] != 0):
                self.board[n] = 0
                self.board[self.PLAYER_SCORE_HOLDER] += 1 + self.board[oponent_pos]
                self.board[oponent_pos] = 0

        return False

    def possible_player_moves(self):
        for i, a in enumerate(self.board[1:self.PLAYER_SCORE_HOLDER]):
            if a > 0:
                yield i

    def get_player_moves(self, pos, seq, moves):
        assert self.board[1 + pos] != 0

        new_board = Board(self)
        move_continue = new_board.make_player_move(pos)

        ###### new ones
        new_board.flip_board()
        ###### new ones

        if move_continue and list(new_board.possible_player_moves()):

            for i in new_board.possible_player_moves():
                new_board.get_player_moves(i, seq + [pos], moves)
        else:
            moves.append((seq + [pos], new_board))
            return

    def find_all_moves(self):
        all_moves = []
        for i in self.possible_player_moves():
            self.get_player_moves(i, [], all_moves)

        return all_moves

    def get_opponent_board(self):
        b = Board()
        b.board = self.board[self.PLAYER_SCORE_HOLDER:] + self.board[:self.PLAYER_SCORE_HOLDER]
        b.reversed = not self.reversed
        return b

    def no_more_moves(self):
        if any(self.board[self.PLAYER_SCORE_HOLDER + 1:]) == False or any(self.board[1:self.PLAYER_SCORE_HOLDER]) == False:
            return True
        else:
            return False

    # def mini_max(self, depth=2, maximizing_player=False):
    #     if depth == 0 or self.no_more_moves():
    #         return self.get_heurestic_score()
    #
    #
    #     if maximizing_player:
    #         best_value = -999
    #         for move, board in self.get_opponent_board().find_all_moves():
    #             val = board.mini_max(depth - 1, not maximizing_player)
    #             best_value = max(best_value, val)
    #         return best_value
    #     else:
    #         best_value = 999
    #         for move, board in self.get_opponent_board().find_all_moves():
    #             val = board.mini_max(depth - 1, not maximizing_player)
    #             best_value = min(best_value, val)
    #         return best_value

    def mini_max_alpha_beta(self, depth=2, alpha=-setup, beta=+setup, maximizing_player=False):
        if depth == 0 or self.no_more_moves():
            return self.get_heurestic_score()
        global node_counter
        if maximizing_player:
            best_value = -setup
            for move, board in self.get_opponent_board().find_all_moves():
                childvalue = board.mini_max_alpha_beta(depth - 1, alpha, beta, not maximizing_player)
                best_value = max(best_value, childvalue)
                alpha = max(alpha, best_value)
                node_counter += 1#counting node

                if beta <= alpha:
                    break
            return best_value
        else:
            best_value = setup
            for move, board in self.get_opponent_board().find_all_moves():
                childvalue = board.mini_max_alpha_beta(depth - 1, not maximizing_player)
                best_value = min(best_value, childvalue)
                beta = min(beta, best_value)
                node_counter += 1#counting node

                if beta <= alpha:
                    break
            return best_value

    def lucky(self,depth = 2):
        if depth == 0 or self.no_more_moves():
            return self.get_heurestic_score()
        move = []
        best_value = -999
        for move, board in self.get_opponent_board().find_all_moves():
                best_value = random.choice(move)
        return best_value

    def find_best_move(self, n=1):
        print("Calculating best move...")
        t = time()

        # def moves():
        #     with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
        #         yield from pool.map(compute, list(self.find_all_moves()))
        allmoves = list(self.find_all_moves())
        tempresult = []
        for move in allmoves:
            tempresult.append(compute(move))
        # result = sorted(moves(), key=lambda x: x[1], reverse=True)[:1]
        result = sorted(tempresult,reverse = True)
        print("Calculated in %.1fs" % (time() - t))
        return result
        # return result

    def print(self):
        print("  ", end="")
        # print("%s|%s|%s|%s".format("Score","Player 1", "Player 2", "Score"))
        print(*["%2d" % x for x in reversed(self.board[self.PLAYER_SCORE_HOLDER + 1:])], sep="|")
        print("%2d %s %2d" % (self.opponent_points," "*MANCALA*3, self.player_points))
        print("  ", end="")
        print(*["%2d" % x for x in self.board[1:self.PLAYER_SCORE_HOLDER ]], sep="|")
   
    def string(self):
        result = StringIO()
        print("  ", end="", file=result)
        print(*["%2d" % x for x in reversed(self.board[self.PLAYER_SCORE_HOLDER +  1:])], sep="|", file=result)
        print("%2d                  %2d" % (self.opponent_points, self.player_points), file=result)
        print("  ", end="", file=result)
        print(*["%2d" % x for x in self.board[1:self.PLAYER_SCORE_HOLDER +  1]], sep="|", file=result)
        return result.getvalue()

    def flip_board(self):
        self.board[MANCALA], self.board[2*(MANCALA+1) - 1] = self.board[2*(MANCALA +1)-1],self.board[MANCALA]

    def get_heurestic_score(self):
        if not self.reversed:
            return self.player_points - self.opponent_points
        else:
            return self.opponent_points - self.player_points

def player_move(board):

    has_move = True
    while has_move:
        # bestmoves = board.find_best_move(2)

        # print(bestmoves)
        # if len(bestmoves) == 0:
        #     print("Game ends")
        #     #print("Game scores player = {}, opponent = {}".format(str(board.player_points),str(board.opponent_points)))
        #     print("Game scores player = {}, opponent = {}".format(str(board.player_points),str(board.opponent_points)))

        #     if int(str(board.player_points)) > int(str(board.opponent_points)):
        #         print("Player Wins")
        #     if int(str(board.player_points)) < int(str(board.opponent_points)):
        #         print("Opponent Wins")
        #     if int(str(board.player_points)) == int(str(board.opponent_points)):
        #         print("Draw!")

        #     sys.exit(0)

        player_board = [1,2,3,4,5,6]
        command = random.choices(player_board)
        
        #command = input('Player move: ').split()
        # move = []
        # for move, board in board.get_opponent_board().find_all_moves():
        #         command = [random.choice(move)]

        # for command in board.get_opponent_board().find_all_moves():
        #     command = random.choice(command)
        #     continue
        if not command:
            continue
        if command[0] == 'q':
            sys.exit(0)

        try:
            c = int(command[0])
            has_move = board.make_player_move(c - 1)
            board.print()
        except:
            print('Wrong move: ', command[0])
            continue

    return board

def opponent_move(board):
    board = board.get_opponent_board()
    has_move = True
    while has_move:
        # command = input('Opponent move: ').split()
        print("Opponent move by computer...")
        bestmoves = board.find_best_move(2)

        print(bestmoves)
        if len(bestmoves) == 0:
            print("Game ends")
            print("Game scores player = {}, opponent = {}".format(str(board.player_points),str(board.opponent_points)))

            if int(str(board.player_points)) > int(str(board.opponent_points)):
                print("Player Wins")
                f.write("Player Wins! \r\n")

            if int(str(board.player_points)) < int(str(board.opponent_points)):
                print("AI Wins")
                f.write("AI Wins! \r\n")

            if int(str(board.player_points)) == int(str(board.opponent_points)):
                print("Draw!")
                f.write("Draw! \r\n")
            sys.exit(0)

        # if not command:
        #     continue
        # if command[0] == 'q':
        #     sys.exit(0)
        try:
            # c = int(command[0])
            c = bestmoves[0][0][0]
            has_move = board.make_player_move(c - 1)
            board.flip_board()
            print("after opponent flip")
            print("done opponent flip")
            board.get_opponent_board().print()
        except:
        #     print('Wrong move: ', command[0])
            continue

    return board.get_opponent_board()

def run_game(initial_board=None, player_starts=True):
    board = Board()
    if initial_board is not None:
        board.board = initial_board

    board.print()
    while 1:
        if player_starts:
            for best_move in board.find_best_move(2):
                print(best_move)
            print("node visited by now {}".format(str(node_counter)))
            board = player_move(board)
            random_choice = random.randint(0,100) % 2

            # if(random_choice == 0):
            print("\t\t\t\tTime to flip")
            board.flip_board()
            print("\t\t\t\after flipping")
            board.print()

            board = opponent_move(board)
            print("node visited by now {}".format(str(node_counter)))

        else:
            board = opponent_move(board)
            for best_move in board.find_best_move(2):
                print(best_move)
            print("node visited by now {}".format(str(node_counter)))

            board = player_move(board)

        if board.no_more_moves():
            print("Games ended")
            print("Game scores player = {}, opponent = {}".format(str(board.player_points),str(board.opponent_points)))
            if int(str(board.player_points)) > int(str(board.opponent_points)):
                print("Player Wins")
                f.write("Player Wins! \r\n")

            if int(str(board.player_points)) < int(str(board.opponent_points)):
                print("AI Wins")
                f.write("AI Wins! \r\n")

            if int(str(board.player_points)) == int(str(board.opponent_points)):
                print("Draw!")
                f.write("Draw! \r\n")


            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Mancala AI')
    parser.add_argument('-b', '--board', default=None)
    parser.add_argument('-d', '--depth', type=int, default=5)
    parser.add_argument('-o', '--opponent-starts', default=False, action="store_true")
    parser.add_argument('--dont-score-one', default=False, action="store_true")
    args = parser.parse_args()

    DEPTH = args.depth
    DONT_SCORE_ONE = args.dont_score_one
    run_game(args.board, not args.opponent_starts)

