#!/usr/bin/env python
# coding: utf-8

# # 五子棋 Q-Learning

# In[1]:


import numpy as np
import copy


class GoBang():
    def __init__(self, width=9, height=9):  # 設定初始參數(棋盤)
        self.width = width
        self.height = height
        self.board = [[' ']*self.width for h in range(self.height)]
        self.player = np.random.choice(["P1", "P2"])
        self.moveRecord = []

    def restart(self):  # 重新開始遊戲
        self.board = [[' ']*self.width for h in range(self.height)]
        self.moveRecord = []
        self.player = np.random.choice(["P1", "P2"])

    def isLegal(self, x, y):  # 檢查這步棋是否合法
        if self.board[x][y] == " ":
            return True
        else:
            return False

    def makeMove(self, token):  # 下棋(token = "O" or "X")
        try:
            draw_location = input(f"請 {self.player} 輸入下棋座標(範例：0,0)：")
            x, y = int(draw_location.split(",")[0]), int(
                draw_location.split(",")[1])
            if self.isLegal(x, y):
                self.board[x][y] = token
                self.moveRecord.append((self.player, x, y))
            else:
                print("illegal move")
                self.makeMove(token)
        except:
            print("請依照範例輸入座標")
            self.makeMove(token)

    def drawBoard(self):  # 畫出棋盤
        HLine = " "*3 + "+---"*self.width + "+"
        axis = " "*5 + "0"
        for i in range(1, self.width):
            axis += " "*3 + str(i)
        print(axis)
        print(HLine)
        for y in range(self.height):
            print(y, end="  ")  # 加上end=" "可以不換行
            for x in range(self.width):
                print(f"| {self.board[y][x]}", end=" ")
            print("|")
            print(HLine)

    def isOver(self, token):  # 判斷遊戲結束
        goal = 5
        # 橫線
        for iy in range(self.height):
            for ix in range(self.width - 4):  # 往後延展四格
                if (self.board[iy][ix:ix+5] == [token]*goal):
                    print(f"Player {self.player} wins!!!")
                    return token

        # 直線(轉置後就變成判斷橫線)
        Tboard = np.array(self.board)
        Tboard = Tboard.T
        for ix in range(self.width):
            for iy in range(self.height - 4):
                if (list(Tboard[ix][iy:iy+5]) == [token]*goal):
                    print(f"Player {self.player} wins!!!")
                    return token

        # 斜線
        longSide = np.max([self.width, self.height])
        for delta_x in range(self.width - 4):
            for delta_y in range(self.height - 4):
                diag = [self.board[ix + delta_y][ix + delta_x]
                        for ix in range(goal)]
                diagAnti = [self.board[ix + delta_y]
                            [longSide - 1 - ix - delta_x] for ix in range(goal)]
                if (diag == [token]*goal) or (diagAnti == [token]*goal):
                    print(f"Player {self.player} wins!!!")
                    return token

        line = []
        for ix in range(longSide):
            line += self.board[ix]
        if " " not in line:
            print("Tie!!!")
            return "0"

        return False

    def play2PlayerGame(self):
        print("歡迎來到雙人下棋峽谷")
        while True:
            self.restart()  # 重置棋盤
            P1_token, P2_token = "○", "●"
            print("P1先手" if self.player == "P1" else "P2先手")

            while True:
                token = P1_token if self.player == "P1" else P2_token
                self.makeMove(token)
                self.drawBoard()
                if self.isOver(token):
                    break
                self.player = "P2" if self.player == "P1" else "P1"  # 換人下棋

            ans = input("輸入'yes'再來一場，輸入其他離開遊戲。")
            if ans == "yes":
                continue
            else:
                print("下次再來玩")
                break

    def play1PlayerGame(self, AI, mode):
        print("歡迎來到單人下棋峽谷")
        while True:
            self.restart()  # 重置棋盤
            P1_token, P2_token = "○", "●"
            print("P1先手" if self.player == "P1" else "P2(AI)先手")

            while True:
                token = P1_token if self.player == "P1" else P2_token
                if self.player == "P1":
                    self.makeMove(token)
                    self.drawBoard()
                else:
                    x, y = AI.getAI_Move(self.board, token=P2_token, mode=mode)
                    print(f"AI輸入下棋座標：{(x,y)}")
                    self.board[x][y] = token
                    self.moveRecord.append(("AI", x, y))
                    self.drawBoard()
                if self.isOver(token):
                    break
                self.player = "P2" if self.player == "P1" else "P1"  # 換人下棋

            ans = input("輸入'y'再來一場，輸入'n'離開遊戲。")
            if ans == "y":
                continue
            else:
                print("下次再來玩")
                break

    def play0PlayerGame(self, AI, P1Mode, P2Mode):
        print("機器對戰模式")
        winRecord = []
        for _ in range(1):
            self.restart()  # 重置棋盤
            P1_token, P2_token = "○", "●"
            print("P1先手" if self.player == "P1" else "P2先手")

            while True:
                token = P1_token if self.player == "P1" else P2_token
                if self.player == "P1":
                    x, y = AI.getAI_Move(self.board, token, P1Mode)
                    print(f"AI(P1)輸入下棋座標：{(x,y)}")
                    self.board[x][y] = token
                    self.moveRecord.append(("AIP1", x, y))
                    self.drawBoard()
                else:
                    x, y = AI.getAI_Move(self.board, token, P2Mode)
                    print(f"AI(P2)輸入下棋座標：{(x,y)}")
                    self.board[x][y] = token
                    self.moveRecord.append(("AIP2", x, y))
                    self.drawBoard()

                winner = self.isOver(token)
                if winner:
                    break

                self.player = "P2" if self.player == "P1" else "P1"  # 換人下棋

            if winner == "0":
                winRecord.append("0")
            else:
                winRecord.append(self.player)

        return winRecord


# In[2]:


class AI_Player(GoBang):
    def __init__(self, width=9, height=9):
        # 取得遊戲棋盤
        super().__init__(width=9, height=9)

    def possibleMoves(self, remainedBoard):  # 取得可下之空位座標
        possibleMovesList = []
        for iy in range(self.height):
            for ix in range(self.width):
                if remainedBoard[iy][ix] == " ":
                    possibleMovesList.append((iy, ix))
        return possibleMovesList

    def isLine(self, remainBoard, goal, token):  # 判斷連子數
        # 橫線
        HLine = 0
        for iy in range(self.height):
            for ix in range(self.width - (goal-1)):  # 往後延展
                if (remainBoard[iy][ix:ix+goal] == [token]*goal):
                    HLine += 1

        # 直線(轉置後就變成判斷橫線)
        VLine = 0
        Tboard = np.array(remainBoard)
        Tboard = Tboard.T
        for ix in range(self.width):
            for iy in range(self.height - (goal-1)):
                if (list(Tboard[ix][iy:iy+goal]) == [token]*goal):
                    VLine += 1

        # 斜線
        DLine = 0
        RDLine = 0
        longSide = np.max([self.width, self.height])
        for delta_x in range(self.width - (goal-1)):
            for delta_y in range(self.height - (goal-1)):
                diag = [remainBoard[ix + delta_y][ix + delta_x]
                        for ix in range(goal)]
                diagAnti = [remainBoard[ix + delta_y]
                            [longSide - 1 - ix - delta_x] for ix in range(goal)]
                if (diag == [token]*goal):
                    DLine += 1
                if (diagAnti == [token]*goal):
                    RDLine += 1

        clf = HLine+VLine+DLine+RDLine
        return clf

    def expertMove(self, remainedBoard, goal, token):  # goal為欲達成的連子數
        possibleMovesList = self.possibleMoves(remainedBoard)
        listLength = len(possibleMovesList)
        oppoToken = "○" if token == "●" else "●"
        lineRecords = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}  # 紀錄1,2,3,4,5連子的數量
        lineRecordsOppo = {0: 0, 1: 0, 2: 0,
                           3: 0, 4: 0, 5: 0}  # 紀錄1,2,3,4,5連子的數量

        if self.isLine(remainedBoard, goal-1, token) or (self.isLine(remainedBoard, goal-1, oppoToken)):
            # 更新我方連子紀錄
            lineRecords[goal-1] = self.isLine(remainedBoard, goal-1, token)
            # 更新對手連子紀錄
            lineRecordsOppo[goal -
                            1] = self.isLine(remainedBoard, goal-1, oppoToken)

            weights = [0, 0, 1, 1, 1, 1]
            points = np.sum(
                np.array(list(lineRecords.values())*np.array(weights)))
            pointsOppo = np.sum(
                np.array(list(lineRecordsOppo.values())*np.array(weights)))
            if points > pointsOppo:
                # 進攻棋步
                for move in possibleMovesList:
                    x, y = move[0], move[1]
                    board_curr = copy.deepcopy(remainedBoard)
                    board_curr[x][y] = token  # AI token
                    newLineRecord = self.isLine(
                        board_curr, goal=goal, token=token)
                    lineRecords_curr = copy.deepcopy(lineRecords)
                    # 更新我方連子紀錄
                    lineRecords_curr[goal -
                                     1] = self.isLine(board_curr, goal-1, token)
                    points_curr = np.sum(
                        np.array(list(lineRecords_curr.values())*np.array(weights)))

                    is_goal = (self.isLine(board_curr, token=token, goal=goal))
                    more_lineRecord = (newLineRecord >= lineRecords[goal])
                    more_points = (points_curr > points)
                    if is_goal and more_lineRecord and more_points:
                        moveIndex = possibleMovesList.index(move)
                        print(f"Attack {goal}", end=" ")
                        return moveIndex
                else:
                    if goal >= 2:
                        print(f"Think Next {goal}", end=" ")
                        return self.expertMove(remainedBoard, goal-1, token)
                    else:
                        print(f"Think Random {goal}", end=" ")
                        return np.random.choice(listLength)
            else:
                # 防守棋步
                for move in possibleMovesList:
                    x, y = move[0], move[1]
                    board_curr = copy.deepcopy(remainedBoard)
                    board_curr[x][y] = oppoToken  # P1 token
                    newLineRecord = self.isLine(
                        board_curr, goal=goal, token=oppoToken)
                    lineRecordsOppo_curr = copy.deepcopy(lineRecordsOppo)
                    # 更新我方連子紀錄
                    lineRecordsOppo_curr[goal -
                                         1] = self.isLine(board_curr, goal-1, oppoToken)
                    pointsOppo_curr = np.sum(
                        np.array(list(lineRecordsOppo_curr.values())*np.array(weights)))

                    is_goal = (self.isLine(
                        board_curr, goal=goal, token=oppoToken))
                    more_lineRecord = (newLineRecord >= lineRecordsOppo[goal])
                    more_points = (pointsOppo_curr > pointsOppo)
                    if is_goal and more_lineRecord and more_points:
                        moveIndex = possibleMovesList.index(move)
                        print(f"Defense {goal}", end=" ")
                        return moveIndex
                else:
                    if goal >= 2:
                        print(f"Think Next {goal}", end=" ")
                        return self.expertMove(remainedBoard, goal-1, token)
                    else:
                        print(f"Think Random {goal}", end=" ")
                        return np.random.choice(listLength)

        else:
            if goal >= 2:
                print(f"Total Next {goal}", end=" ")
                return self.expertMove(remainedBoard, goal-1, token)
            else:
                print(f"Total Random {goal}", end=" ")
                return np.random.choice(listLength)

    def evaluate(self, remainedBoard, side):
        token = "○" if side == "P1" else "●"
        score = 0
        for g in range(1, 5):
            add_score = self.isLine(remainedBoard, g, token)
            if add_score:
                score += g

        token = "○" if token == "●" else "○"
        for b in range(1, 5):
            minus_score = self.isLine(remainedBoard, b, token)
            if minus_score:
                score -= b
        return score

    def min_max_alpha_beta(self, remainedBoard, side, max_depth, alpha=-10e20, beta=10e20):
        """
        Runs the min_max_algorithm on a given board_sate for a given side, to a given depth in order to find the best move
        Args:
            alpha: float
            beta: float
        Returns:
            best_score, best_score_move
        """
        best_score_move = None
        possibleMovesList = self.possibleMoves(remainedBoard)
        if not possibleMovesList:
            return 0, None

        for move in possibleMovesList:
            x, y = move[0], move[1]
            board_curr = copy.deepcopy(remainedBoard)
            board_curr[x][y] = "○" if side == "P1" else "●"  # 新狀態
            winner = self.isOver(board_curr)
            if winner == "0" or winner == False:  # 平手
                winner = 0
            elif winner == "○":  # P1獲勝
                winner = 1
            else:  # P2獲勝
                winner = -1

            if winner != 0:
                return winner * 10e10, move
            else:
                if max_depth <= 1:
                    score = self.evaluate(remainedBoard=board_curr, side=side)
                else:
                    side = "P1" if side == "P2" else "P1"  # 換人下棋
                    score, _ = self.min_max_alpha_beta(
                        board_curr, side, max_depth - 1, alpha, beta)

            if side == "P1":
                if score > alpha:
                    alpha = score
                    best_score_move = move
            else:
                if score < beta:
                    beta = score
                    best_score_move = move
            if alpha >= beta:
                break

        return alpha if side == "P1" else beta, best_score_move

    def getAI_Move(self, remainedBoard, token, mode="expert"):  # AI使用策略有random, expert, minmax
        possibleMovesList = self.possibleMoves(remainedBoard)
        listLength = len(possibleMovesList)
        if mode == "expert":
            moveIndex = self.expertMove(remainedBoard, goal=5, token=token)
            move = possibleMovesList[moveIndex]
        elif mode == "minmax":
            side = self.player
            best_score, move = self.min_max_alpha_beta(
                remainedBoard, side, max_depth=2)
        else:
            moveIndex = np.random.choice(listLength)
            move = possibleMovesList[moveIndex]
        return move


def randomBoard(long=9):
    return [[np.random.choice([" ", "○", "●"]) for _ in range(long)] for _ in range(long)]


if __name__ == '__main__':
    Game = GoBang()
    AI = AI_Player(Game)
    #print(AI.min_max_alpha_beta(randomBoard(), "P1", 2))
    Game.play1PlayerGame(AI, "expert")
    #Game.play0PlayerGame(AI, "minmax", "random")
