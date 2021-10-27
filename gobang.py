import copy
from enum import Enum

inf = 999999999999 

pattern_score = \
{
    # 五个子中有一个子
    (1, 0, 0, 0, 0) : 1,
    (0, 1, 0, 0, 0) : 2,
    (0, 0, 1, 0, 0) : 3,
    (0, 0, 0, 1, 0) : 2,
    (0, 0, 0, 0, 1) : 1,
    # 五个字中有两个子
    (1, 1, 0, 0, 0) : 60,
    (1, 0, 1, 0, 0) : 50,
    (1, 0, 0, 1, 0) : 30,
    (1, 0, 0, 0, 1) : 10,
    (0, 1, 1, 0, 0) : 100,
    (0, 1, 0, 1, 0) : 80,
    (0, 1, 0, 0, 1) : 30,
    (0, 0, 1, 1, 0) : 100,
    (0, 0, 1, 0, 1) : 50,
    (0, 0, 0, 1, 1) : 60,
    # 五个字中有三个子
    (0, 0, 1, 1, 1) : 600,
    (0, 1, 0, 1, 1) : 600,
    (0, 1, 1, 0, 1) : 800,
    (0, 1, 1, 1, 0) : 1000,
    (1, 0, 0, 1, 1) : 400,
    (1, 0, 1, 0, 1) : 300,
    (1, 0, 1, 1, 0) : 800,
    (1, 1, 0, 0, 1) : 400,
    (1, 1, 0, 1, 0) : 600,
    (1, 1, 1, 0, 0) : 600,
    # 五个子中有四个子
    (0, 1, 1, 1, 1) : 5000,
    (1, 0, 1, 1, 1) : 5000,
    (1, 1, 0, 1, 1) : 5000,
    (1, 1, 1, 0, 1) : 5000,
    (1, 1, 1, 1, 0) : 5000,
    # 五个子中有五个字
    (1, 1, 1, 1, 1) : inf
}

class Player(Enum):
    human = 0
    ai = 1

class State(Enum):
    ai_win = 0
    human_win = 1
    tie = 2
    on = 3

class ChessBoard(object):

    def __init__(self, size=19):
        self.board_size = size
        row = [0] * self.board_size
        self.board = []
        for i in range(self.board_size):
            self.board.append(row.copy())

    def pos_in_board(self, x, y):
        return x >= 0 and y >= 0 and x < self.board_size and y < self.board_size

    def pos_is_empty(self, x, y):
        return self.board[x][y] == 0

    def play(self, x, y, player):
        if self.pos_in_board(x, y) and self.pos_is_empty(x, y):
            if player == Player.human:
                self.board[x][y] = -1
            else:
                self.board[x][y] = 1
            return True
        else:
            print("请在合法位置落子")
            return False

    def evaluate(self):
        res = 0
        for i in range(self.board_size):
            for j in range(self.board_size):
                if(self.pos_in_board(i, j+4)):  # 横排五子的左端
                    pattern = []
                    m_pattern = []
                    for k in range(5):
                        pattern.append(self.board[i][j+k])
                        m_pattern.append(-self.board[i][j+k])
                    if pattern_score.get(tuple(pattern)) != None:
                        res = res + pattern_score.get(tuple(pattern))
                    if pattern_score.get(tuple(m_pattern)) != None:
                        res = res - pattern_score.get(tuple(m_pattern))
                if(self.pos_in_board(i+4, j)):  # 竖排五子的上端
                    pattern = []
                    m_pattern = []
                    for k in range(5):
                        pattern.append(self.board[i+k][j])
                        m_pattern.append(-self.board[i+k][j])
                    if pattern_score.get(tuple(pattern)) != None:
                        res = res + pattern_score.get(tuple(pattern))
                    if pattern_score.get(tuple(m_pattern)) != None:
                        res = res - pattern_score.get(tuple(m_pattern))
                if(self.pos_in_board(i+4, j+4)):  # 右斜五子的上端
                    pattern = []
                    m_pattern  =[]
                    for k in range(5):
                        pattern.append(self.board[i+k][j+k])
                        m_pattern.append(-self.board[i+k][j+k])
                    if pattern_score.get(tuple(pattern)) != None:
                        res = res + pattern_score.get(tuple(pattern))
                    if pattern_score.get(tuple(m_pattern)) != None:
                        res = res - pattern_score.get(tuple(m_pattern))
                if(self.pos_in_board(i+4, j-4)):  # 左斜五子的上端
                    pattern = []
                    m_pattern = []
                    for k in range(5):
                        pattern.append(self.board[i+k][j-k])
                        m_pattern.append(-self.board[i+k][j-k])
                    if pattern_score.get(tuple(pattern)) != None :
                        res = res + pattern_score.get(tuple(pattern))
                    if pattern_score.get(tuple(m_pattern)) != None:
                        res = res - pattern_score.get(tuple(m_pattern))
        return res

    def play_evaluate_debug(self):
        while(True):
            player, x, y = input().split()
            x = eval(x)
            y = eval(y)
            if(player == "ai"):
                player = Player.ai
            else:
                player = Player.human
            self.play(x, y, player)
            print(self.evaluate())

    def state(self):
        full = True
        for i in range(self.board_size):
            for j in range(self.board_size):
                if(self.board[i][j] == 0):
                    full = False
                    continue
                if(self.pos_in_board(i, j+4)):  # 横排五子的左端
                    win = True
                    for k in range(5):
                        if self.board[i][j+k] != self.board[i][j]:
                            win = False
                            break
                    if win:
                        if self.board[i][j] == 1:
                            return State.ai_win
                        else:
                            return State.human_win
                if(self.pos_in_board(i+4, j)):  # 竖排五子的上端
                    win = True
                    for k in range(5):
                        if self.board[i+k][j] != self.board[i][j]:
                            win = False
                            break
                    if win:
                        if self.board[i][j] == 1:
                            return State.ai_win
                        else:
                            return State.human_win
                if(self.pos_in_board(i+4, j+4)):  # 右斜五子的上端
                    win = True
                    for k in range(5):
                        if self.board[i+k][j+k] != self.board[i][j]:
                            win = False
                            break
                    if win:
                        if self.board[i][j] == 1:
                            return State.ai_win
                        else:
                            return State.human_win
                if(self.pos_in_board(i+4, j-4)):  # 左斜五子的上端
                    win = True
                    for k in range(5):
                        if self.board[i-k][j+k] != self.board[i][j]:
                            win = False
                            break
                    if win:
                        if self.board[i][j] == 1:
                            return State.ai_win
                        else:
                            return State.human_win
        if full:
            return State.tie
        return State.on

class AI_1(object):
    
    def work(self, chess_board):
        tmp = copy.deepcopy(chess_board)
        x, y, _x, _y = self.max_step(-inf, tmp)
        return x, y, _x, _y

    def max_step(self, now, tmp):
        x = 0
        y = 0
        _x = 0
        _y = 0
        for i in range(tmp.board_size):
            for j in range(tmp.board_size):
                if tmp.pos_in_board(i, j) and tmp.pos_is_empty(i, j):
                    tmp.play(i, j, Player.ai)
                    new_max, px, py = self.min_step(now, tmp)
                    if(new_max > now):
                        x = i
                        y = j
                        _x = px
                        _y = py
                        now = new_max
                    tmp.board[i][j] = 0
                    # print(i, j, new_max)
        return x, y, _x, _y

    def min_step(self, now, tmp):
        res = inf
        x = 0
        y = 0
        for i in range(tmp.board_size):
            for j in range(tmp.board_size):
                if tmp.pos_in_board(i, j) and tmp.pos_is_empty(i, j):
                    tmp.play(i, j, Player.human)
                    score = tmp.evaluate()
                    tmp.board[i][j] = 0
                    if score < res:
                        res = score
                        x, y = i, j
                    if res < now:
                        return now, x, y

        return res, x, y

def human_move(chess_board):
    x, y = input("请输入落子位置").split()
    x = eval(x)
    y = eval(y)
    while not chess_board.play(x, y, Player.human):
        x, y = input("请输入落子位置").split() 
        x = eval(x)
        y = eval(y)

def draw(chess_board):
    print ('  0 1 2 3 4 5 6 7 8 9')
    mark = ('. ', 'O ', 'X ')
    for row in range(chess_board.board_size):
        print (chr(ord('0') + row), end=' ')
        for col in range(chess_board.board_size):
            ch = chess_board.board[row][col]
            if ch == 0: 
                print ('.', end=' ')
            elif ch == 1:
                print ('O', end=' ')
            elif ch == -1:
                print ('X', end=' ')
        print ('')

def play_gobang(first, size=10):
    goBang = ChessBoard(size) 
    ai = AI_1()
    if first == Player.human:
        human_move(goBang)
    while True:
        x, y, _x, _y = ai.work(goBang)
        goBang.play(x, y, Player.ai)
        draw(goBang)
        print("电脑落子在{},{}".format(x, y))
        if goBang.state() != State.on:
            print("游戏结束！")
            break
        human_move(goBang)
        if goBang.state() != State.on:
            print("游戏结束！")
            break

play_gobang(Player.ai)