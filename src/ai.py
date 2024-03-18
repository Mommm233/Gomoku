# ai算法类
from my_enum import Color
from chessboard import  Chessboard

Live_five = 100000
Live_four = 10000
Live_three = 1000
Live_two = 100
Live_one = 10
Death_four = 1000
Death_three = 100
Death_two = 10

class Ai:
    def __init__(self, chessboard:Chessboard, depth:int) -> None:
        self.chessboard = chessboard
        self.depth = depth
        self.best_step  = (-1, -1)

    def grid_to_str(self) -> str:
        grid_string = ""
        for row in self.chessboard.grid:
            for col in row:
                grid_string += str(col)
        str_grid = []
        length = len(grid_string)
        # 水平方向
        i = 0
        while i < length:
            str_grid.append(grid_string[i:i + self.chessboard.width])
            i += self.chessboard.width
        # 竖直方向
        i = 0
        while i < self.chessboard.width:
            str_grid.append(grid_string[i:length:self.chessboard.width])
            i += 1
        # 左上到右下
        i = 0
        while i < self.chessboard.width - 4:
            str_grid.append(grid_string[i:(self.chessboard.height-i)*self.chessboard.width:self.chessboard.width+1])
            i += 1
        i = 1
        while i < self.chessboard.height-4:
            str_grid.append(grid_string[i*self.chessboard.width:length:self.chessboard.width+1])
            i += 1
        # 左下到右上
        i = 4
        while i < self.chessboard.width:
            str_grid.append(grid_string[i:i*self.chessboard.width+1:self.chessboard.width-1])
            i += 1
        i = 1
        while i < self.chessboard.height - 4:
            str_grid.append(grid_string[(i+1)*self.chessboard.width-1:length:self.chessboard.width-1])
            i += 1

        return str_grid

    def evaluate(self, color:Color, next_color:Color) -> float:
        str_grid = self.grid_to_str()
        next_color_score = 0
        color_score = 0
        for i in str_grid:
            if str(next_color.value)*5 in i:
                return -Live_five   # 对手胜利
            if str(color.value)*5 in i:
                return Live_five    # 我方胜利
            
            next_color_score += Live_four * i.count("0" + str(next_color.value) * 4 + "0")
            next_color_score += Live_three * i.count("0" + str(next_color.value) * 3 + "0")
            next_color_score += Live_two * i.count("0" + str(next_color.value) * 2 + "0")
            next_color_score += Live_one * i.count("0" + str(next_color.value) * 1 + "0")
            next_color_score += Death_four * (i.count(str(color.value) + str(next_color.value) * 4 + "0") + i.count("0" + str(next_color.value) * 4 + str(color.value))) 
            next_color_score += Death_three * (i.count(str(color.value) + str(next_color.value) * 3 + "0") + i.count("0" + str(next_color.value) * 3 + str(color.value))) 
            next_color_score += Death_two * (i.count(str(color.value) + str(next_color.value) * 2 + "0") + i.count("0" + str(next_color.value) * 2 + str(color.value))) 
    
            color_score += 3 * Live_four * 0.5 * i.count(str(color.value) * 2 + "0" + str(color.value) * 2)
            color_score += 3 * Live_four * 0.5 * i.count(str(color.value) + "0" + str(color.value) * 3)
            color_score += 3 * Live_four * 0.5 * i.count(str(color.value) * 3 + "0" + str(color.value))
            color_score += 3 * Live_three * 0.5 * i.count("0" + str(color.value) + "0" + str(color.value) * 2 + "0")
            color_score += 3 * Live_three * 0.5 * i.count("0" + str(color.value) * 2 + "0" + str(color.value) + "0")
            
            color_score += 3 * Live_four * i.count("0"  + str(color.value) * 4 + "0" )  # 计算活四的个数
            color_score += 3 * Live_three * i.count("0"  + str(color.value) * 3 + "0" )  # 计算活三的个数
            color_score += 3 * Live_two * i.count("0"  + str(color.value) * 2 + "0" )  # 计算活二的个数
            color_score += 3 * Live_one * i.count("0"  + str(color.value) * 1 + "0" )  # 计算活一的个数
            color_score += 13 * Death_four * (i.count(str(next_color.value) + str(color.value) * 4 + "0" ) + i.count("0"  + str(color.value) * 4 + str(next_color.value)))
            color_score += 3 * Death_three * (i.count(str(next_color.value) + str(color.value) * 3 + "0" ) + i.count("0"  + str(color.value) * 3 + str(next_color.value)))
            color_score += 3 * Death_two * (i.count(str(next_color.value) + str(color.value) * 2 + "0" ) + i.count("0"  + str(color.value) * 2 + str(next_color.value)))

        return color_score - next_color_score
    
    # Alpha-Beta剪枝算法
    def alpha_beta_pruning(self, color:Color, next_color:Color, depth:int, alpha:float, beta:float, is_ai:bool) -> float:
        if is_ai:
            color = Color.BLACK
            next_color = Color.WHITE
        else:
            color = Color.WHITE
            next_color = Color.BLACK

        if depth <= 0:
            return self.evaluate(color, next_color)

        score = self.evaluate(color, next_color)
        if abs(score) >= Live_five: # 已经产生胜者
            return score

        best_score = -10000
        steps = self.potential_step()
        if len(steps) <= 0:
           return
        best_step = steps[0]

        for (i, j) in steps:
            self.chessboard.drop_piece(i, j, color)
            score = -self.alpha_beta_pruning(next_color, color, depth-1, -beta, -alpha, not is_ai)
            self.chessboard.drop_piece(i, j, Color.BLANK)
            
            if is_ai:
                alpha = max(alpha, score)
                if alpha >= beta:
                    break
            else:
                beta = min(beta, score)
                if beta <= alpha:
                    break

            if score > best_score:
                best_score = score
                best_step = (i, j)

        if depth == self.depth:
            self.best_step = best_step
        
        return best_score

    def potential_step(self) -> list[tuple]:
        # 返回潜在的位置
        steps = []
        dir = ((-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1))
        
        for i in range(self.chessboard.height):
            for j in range(self.chessboard.width):
                if self.chessboard.grid[i][j] == Color.BLANK.value:
                    for d in dir:
                        if i + d[0] >= 0 and i + d[0] < self.chessboard.height and j + d[1] >= 0 and j + d[1] < self.chessboard.width:
                            if self.chessboard.grid[i + d[0]][j + d[1]] != Color.BLANK.value:
                                steps.append((i, j))
        return steps

    # 获取AI的下棋位置
    def get_ai_move(self) -> tuple:
        best_score = self.alpha_beta_pruning(Color.BLACK, Color.WHITE, self.depth, float('-inf'), float('inf'), True)
        if self.best_step[0] == -1:
            for i in range(self.chessboard.height):
                for j in range(self.chessboard.width):
                    if self.chessboard.grid[i][j] == Color.BLANK:
                        return (i, j)
        return self.best_step


