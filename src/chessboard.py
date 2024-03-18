# 棋盘类
from my_enum import Color, Player


class Chessboard:
    def __init__(self, height:int, width:int) -> None:
        self.height = height
        self.width = width
        # grid 网格
        self.grid = [[Color.BLANK.value] * width for _ in range(height)]
        # 先下一黑子
        self.grid[height // 2][width // 2] = Color.BLACK.value
        # 检查盘面是否下满棋子
        self.full = 1

        self.player = Player.HUMAN

    def init(self) -> None:
        # grid 网格
        self.grid = [[Color.BLANK.value] * self.width for _ in range(self.height)]
        # 先下一黑子
        self.grid[self.height // 2][self.width // 2] = Color.BLACK.value
        # 检查盘面是否下满棋子
        self.full = 1

        self.player = Player.HUMAN

    # 返回(判断，轨迹)
    def is_win(self, color:Color) -> tuple[bool, list[tuple]]: 
        for i in range(self.height):
            for j in range(self.width):
                if self.grid[i][j] != color.value:
                    continue
                # Check horizontally
                if j + 4 < self.width and all(self.grid[i][j+k] == color.value for k in range(1, 5)):
                    return (True, [(i, j+k) for k in range(5)])
                # Check vertically
                if i + 4 < self.height and all(self.grid[i+k][j] == color.value for k in range(1, 5)):
                    return (True, [(i+k, j) for k in range(5)])
                # Check diagonally (down-right)
                if i + 4 < self.height and j + 4 < self.width and all(self.grid[i+k][j+k] == color.value for k in range(1, 5)):
                    return (True, [(i+k, j+k) for k in range(5)])
                # Check diagonally (down-left)
                if i + 4 < self.height and j - 4 >= 0 and all(self.grid[i+k][j-k] == color.value for k in range(1, 5)):
                    return (True, [(i+k, j-k) for k in range(5)])
        return (False, [])

    def is_full(self) ->bool:  # 判断棋盘是否满子了
        return self.full == self.height * self.width

    # 落子
    def drop_piece(self, i:int, j:int, color:Color) -> None: 
        self.grid[i][j] = color.value
        if color != Color.BLANK:
            self.full += 1
        else:
            self.full -= 1

    # def inverse_grid(self):
    #     for i in range(self.height):
    #         for j in range(self.width):
    #             if self.grid[i][j] == Color.BLACK:
    #                 self.grid[i][j] = Color.WHITE
    #             elif self.grid[i][j] == Color.WHITE:
    #                 self.grid[i][j] = Color.BLACK
    