import copy
import math
import random
import time
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

board_size = 8

black = 1
white = 2

up = 0
right = 1
down = 2
left = 3
up_right = 5
up_left = 6
down_left = 7
down_right = 8

exploration_param = math.sqrt(2)


probability_board = [
    [32, 2, 16, 8, 8, 16, 2, 32],
    [2, 1, 2, 4, 4, 2, 1, 2],
    [16, 2, 16, 8, 8, 16, 2, 8],
    [8, 4, 8, 4, 4, 8, 4, 8],
    [8, 4, 8, 4, 4, 8, 4, 8],
    [16, 2, 16, 8, 8, 16, 2, 16],
    [2, 1, 2, 4, 4, 2, 1, 2],
    [32, 2, 16, 8, 8, 16, 2, 32]
]

def opponent(player):
    return black if player == white else white

def sign(player):
    return -1 if player == white else 1

class Game:
    def __init__(self):
        self.board = []
        for x in range(board_size):
            self.board.append([0] * board_size)
        self.board[3][3] = white
        self.board[3][4] = black
        self.board[4][3] = black
        self.board[4][4] = white
        self.turn = black
        self.size = 4
        self.no_move_count = 0
        self.next_moves = set()
        for x in range(2, 6):
            for y in range(2, 6):
                if x == 2 or y == 2 or x == 5 or y == 5:
                    self.next_moves.add((x, y))
    
    def get_moves(self):
        ret_ar = []
        for x, y in self.next_moves:
                if(len(self.valid_moves(x, y)) > 0):
                    ret_ar.append((x, y))
        if(len(ret_ar) == 0):
            ret_ar.append(None)
        return ret_ar

    def valid_moves(self, x, y):
        if(self.board[x][y] != 0):
            return []
        ret_ar = []
        if(x + 1 < board_size and self.board[x+1][y] == opponent(self.turn)):
            for x1 in range(x+2, board_size):
                if(self.board[x1][y] == 0):
                    break
                elif(self.board[x1][y] == self.turn):
                    ret_ar.append(right)
                    break
        if(x > 0 and self.board[x-1][y] == opponent(self.turn)):
            for x1 in range(x-2, -1, -1):
                if(self.board[x1][y] == 0):
                    break
                elif(self.board[x1][y] == self.turn):
                    ret_ar.append(left)
                    break
        if(y + 1 < board_size and self.board[x][y+1] == opponent(self.turn)):
            for y1 in range(y+2, board_size):
                if(self.board[x][y1] == 0):
                    break
                elif(self.board[x][y1] == self.turn):
                    ret_ar.append(down)
                    break
        if(y > 0 and self.board[x][y-1] == opponent(self.turn)):
            for y1 in range(y-2, -1, -1):
                if(self.board[x][y1] == 0):
                    break
                elif(self.board[x][y1] == self.turn):
                    ret_ar.append(up)
                    break
        if(y > 0 and x > 0 and self.board[x-1][y-1] == opponent(self.turn)):
            for c in range(2, min(x+1, y+1)):
                if(self.board[x-c][y-c] == 0):
                    break
                elif(self.board[x-c][y-c] == self.turn):
                    ret_ar.append(up_left)
                    break
        if(y + 1 < board_size and x + 1  < board_size and self.board[x+1][y+1] == opponent(self.turn)):
            for c in range(2, min(board_size-x, board_size-y)):
                if(self.board[x+c][y+c] == 0):
                    break
                elif(self.board[x+c][y+c] == self.turn):
                    ret_ar.append(down_right)
                    break
        if(y + 1 < board_size and x > 0 and self.board[x-1][y+1] == opponent(self.turn)):
            for c in range(2, min(x + 1, board_size-y)):
                if(self.board[x-c][y+c] == 0):
                    break
                elif(self.board[x-c][y+c] == self.turn):
                    ret_ar.append(down_left)
                    break
        if(y > 0 and x + 1  < board_size and self.board[x+1][y-1] == opponent(self.turn)):
            for c in range(2, min(board_size-x, y+1)):
                if(self.board[x+c][y-c] == 0):
                    break
                elif(self.board[x+c][y-c] == self.turn):
                    ret_ar.append(up_right)
                    break
        return ret_ar

    def make_move(self, move, moves=None):
        if(move != None and move[0] != -1):
            x = move[0]
            y = move[1]
            if(moves == None):
                moves = self.valid_moves(x, y)
            self.next_moves.remove((x, y))
            self.board[x][y] = self.turn
            for x1 in range(-1, 2):
                for y1 in range(-1, 2):
                    if(x+x1>=0 and x+x1<board_size and y+y1>=0 and y+y1<board_size and self.board[x+x1][y+y1] == 0):
                        self.next_moves.add((x+x1,y+y1))
            if(right in moves):
                for x1 in range(x+1, board_size):
                    if(self.board[x1][y] == self.turn):
                        break
                    self.board[x1][y] = self.turn
            if(left in moves):
                for x1 in range(x-1, -1, -1):
                    if(self.board[x1][y] == self.turn):
                        break
                    self.board[x1][y] = self.turn
            if(up in moves):
                for y1 in range(y-1, -1, -1):
                    if(self.board[x][y1] == self.turn):
                        break
                    self.board[x][y1] = self.turn
            if(down in moves):
                for y1 in range(y+1, board_size):
                    if(self.board[x][y1] == self.turn):
                        break
                    self.board[x][y1] = self.turn
            if(up_left in moves):
                for c in range(1, min(x+1, y+1)):
                    if(self.board[x-c][y-c] == self.turn):
                        break
                    self.board[x-c][y-c] = self.turn
            if(up_right in moves):
                for c in range(1, min(board_size-x, y+1)):
                    if(self.board[x+c][y-c] == self.turn):
                        break
                    self.board[x+c][y-c] = self.turn
            if(down_left in moves):
                for c in range(1, min(x + 1, board_size-y)):
                    if(self.board[x-c][y+c] == self.turn):
                        break
                    self.board[x-c][y+c] = self.turn
            if(down_right in moves):
                for c in range(1, min(board_size-x, board_size-y)):
                    if(self.board[x+c][y+c] == self.turn):
                        break
                    self.board[x+c][y+c] = self.turn
            self.size += 1
            self.no_move_count = 0
        else:
            self.no_move_count += 1
        self.turn = opponent(self.turn)

    def can_move(self):
        return not None in self.get_moves()
    
    def get_winner(self):
        if(not (self.size == board_size*board_size or self.no_move_count == 2)):
            return 0
        white_score = 0
        black_score = 0
        for x in range(board_size):
            for y in range(board_size):
                if(self.board[x][y] == white):
                    white_score+=1
                elif(self.board[x][y] == black):
                    black_score+=1
        if(white_score > black_score):
            return white
        elif(white_score == black_score):
            return random.randint(1, 2)
        else:
            return black

    def print(self):
        print(" 12345678")
        for x in range(board_size):
            s = str(x+1)
            for y in range(board_size):
                if(self.board[x][y] == 0):
                    s += "."
                elif(self.board[x][y] == white):
                    s += "O"
                else:
                    s += "X"
            print(s)
        print(self.next_moves)

    def get_hueristic(self, x):
        if(x == None):
            return 0
        prob = probability_board[x[0]][x[1]]
        if(type(prob) == int):
            return prob
        else:
            return prob[1] if self.board[prob[0]][prob[1]] == opponent(self.turn) else prob[2]
            

class Tree:
    def __init__(self, player, move, moves, heuristic):
        self.edges = []
        self.parent = None
        self.numerator = 0
        self.denominator = 0
        self.move = move
        self.player = player
        self.moves = moves
        self.heuristic = heuristic

    def print(self):
        print(self.numerator, self.denominator, self.move, self.player)
    
    def printTree(self, num, limit):
        if (num == limit):
            return
        for x in range(num):
            print("-", end="")
        print(">", end="")
        self.print()
        for x in self.edges:
            x.printTree(num+1, limit)

class MonteCarlo:
    def __init__(self):
        self.game = Game()
        self.tree = tree

    def make_move(self, move):
        self.game.make_move(move)
        for x in self.tree.edges:
            if(x.move == move):
                self.tree = x
                return
    
    def iterate(self):
        t = time.time()
        while(time.time() - t <= 2):
            self.game_copy = copy.deepcopy(self.game)
            selection_node = self.selection(self.tree)
            if(self.game_copy.get_winner() > 0):
                expansion_node = selection_node
            else:
                expansion_node = self.expansion(selection_node)
            simulation_node = self.simulation(expansion_node)
            self.back_propagation(simulation_node)

    def best_move(self):
        max_value = -1
        max_node = None
        for x in self.tree.edges:
            if x.denominator > max_value:
                max_value = x.denominator
                max_node = x
        return max_node.move


    def selection(self, node):
        if(len(node.edges) != len(node.moves)):
            return node
        max_value = -math.inf
        max_node = 0
        for x in node.edges:
            value = (x.numerator+64*x.heuristic) / x.denominator + exploration_param * math.sqrt(math.log(node.denominator) / x.denominator)
            if(value > max_value):
                max_value = value
                max_node = x
        self.game_copy.make_move(max_node.move)
        return self.selection(max_node)

    def expansion(self, node):
        explored_moves = set()
        for x in node.edges:
            explored_moves.add(x.move)
        while(True):
            x = random.choice(node.moves)
            if(not x in explored_moves):
                self.game_copy.make_move(x)
                ret = Tree(self.game_copy.turn, x, self.game_copy.get_moves(), self.game_copy.get_hueristic(x))
                node.edges.append(ret)
                ret.parent = node
                return ret

    def simulation(self, node):
        while(True):
            winner = self.game_copy.get_winner()
            if(winner > 0):
                node.denominator = 1
                node.numerator = 0 if node.player == winner else 1
                break
            move = random.choice(node.moves)
            self.game_copy.make_move(move)
            ret = Tree(self.game_copy.turn, move, self.game_copy.get_moves(), self.game_copy.get_hueristic(move))
            node.edges.append(ret)
            ret.parent = node
            node = ret
        return node

    
    def back_propagation(self, node):
        node_copy = copy.copy(node)
        node_copy = node_copy.parent
        while(node_copy != None):
            node_copy.numerator += node.numerator if node.player == node_copy.player else 1 - node.numerator
            node_copy.denominator += 1
            node_copy = node_copy.parent

def play():
    print("Welcome")
    simulation = MonteCarlo()
    while(True):
        winner = simulation.game.get_winner()
        if(winner > 0):
            print("WINNER: " + ("black" if winner == black else "white"))
            break
        if(simulation.game.turn == black):
            moves = simulation.game.get_moves()
            if(None in moves):
                simulation.game.make_move(None)
                continue
            simulation.game.print()

            while(True):
                x = int(input("Enter x-coordinate:")) - 1
                y = int(input("Enter y-coordinate:")) - 1
                if((x, y) in moves):
                    simulation.game.make_move((x, y))
                    simulation.game.print()
                    break
                print("Invalid Input!")
        else:
            simulation.iterate()
            move = simulation.best_move()
            if(move == None):
                print("White can't move")
            else:
                print("White makes move: " + str(move[0]+1) + " " + str(move[1]+1))
            simulation.game.make_move(move)

@app.route("/make_move", methods=['POST'])
def make_move_req():
    global simulations
    id = request.json["id"]
    print(type(id), simulations)
    if(len(request.json["move"]) == 0):
        simulations[id].make_move(None)
    elif(len(simulations[id].game.valid_moves(request.json["move"][0], request.json["move"][1])) > 0):
        simulations[id].make_move((request.json["move"][0], request.json["move"][1]))
    else:
        return jsonify({"board": simulations[id].game.board, "winner": simulations[id].game.get_winner(), "move": [], "turn": simulations[id].game.turn, "canMove": simulations[id].game.can_move(), "id": id})
    return jsonify({"board": simulations[id].game.board, "winner": simulations[id].game.get_winner(), "move": request.json["move"], "turn": simulations[id].game.turn, "canMove": simulations[id].game.can_move(), "id": id})

@app.route("/get_move", methods=['POST'])
def get_move_req():
    global simulations
    id = request.json["id"]
    simulations[id].iterate()
    #simulations[id].tree.printTree(0, 3)
    move = simulations[id].best_move()
    simulations[id].make_move(move)
    return jsonify({"board": simulations[id].game.board, "winner": simulations[id].game.get_winner(), "move": [0] if move == None else [move[0], move[1]], "turn": simulations[id].game.turn, "canMove": simulations[id].game.can_move(), "id": id})

@app.route("/start_game", methods=['POST'])
def start_game():
    global simulations
    global next_id
    id = next_id
    next_id += 1
    simulations[id] = MonteCarlo()
    return jsonify({"board": simulations[id].game.board, "winner": simulations[id].game.get_winner(), "move": [], "turn": simulations[id].game.turn, "canMove": True, "id": id})

@app.route("/")
def index():
    return render_template("main.html")

def init():
    global tree
    global simulations
    global next_id
    sample_game = Game()
    tree = Tree(sample_game.turn, None, sample_game.get_moves(), None)
    simulations = dict()
    simulations[0] = MonteCarlo()
    simulations[0].iterate()
    next_id = 1







                
                


        

