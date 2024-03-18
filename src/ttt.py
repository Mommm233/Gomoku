import pygame
import sys
import multiprocessing
from my_enum import Color, Player
from chessboard import Chessboard
from ai import Ai
from button import Button
from audio import Audio

# 设置颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)


def coordinate_to_idx(pos: tuple, error=10) -> tuple:
    x, y = pos
    i = (y - 50 + error) // 50
    j = (x - 50 + error) // 50
    if i >= 0 and i <= 10 and j >= 0 and j <= 10:
        return (i, j)
    return (-1, -1)


def draw_grid() -> None: # 画棋盘线
    for i in range(1, 12):
        # (width, height)
        pygame.draw.line(screen, BLACK, (50, i * 50), (550, i * 50), 2)  # 水平线
        pygame.draw.line(screen, BLACK, (i * 50, 50), (i * 50, 550), 2)  # 垂直线


def draw_stone() -> None: # 画棋子
    recent_pos1 = None
    recent_pos2 = None
    if len(pos_list) >= 1:
        recent_pos1 = pos_list[-1]
    if len(pos_list) >= 2:
        recent_pos2 = pos_list[-2]

    for i in range(chessboard.height):
        for j in range(chessboard.width):
            if chessboard.grid[i][j] == Color.BLANK.value:
                continue
            
            pygame.draw.circle(screen, 
                                WHITE if chessboard.grid[i][j] == Color.WHITE.value else BLACK, 
                                ((j + 1) * 50, (i + 1) * 50), 
                                20)
            # 绘制标记
            if recent_pos1 and (i, j) == recent_pos1:
                pygame.draw.circle(screen, BLUE, ((j + 1) * 50, (i + 1) * 50), 5)
            if recent_pos2 and (i, j) == recent_pos2:
                pygame.draw.circle(screen, BLUE, ((j + 1) * 50, (i + 1) * 50), 5)


def draw_button() -> None: # 绘制按钮
    for img, rect in button.button_dict.values():
        # print(img, rect)
        screen.blit(img, rect)


def draw_trajectory() -> None: # 画轨迹
    if chessboard.player == Player.AI:
        trajectory = chessboard.is_win(Color.WHITE)[1]
    else:
        trajectory = chessboard.is_win(Color.BLACK)[1]
    if len(trajectory) >= 2:
        modified_trajectory = [((point[1] + 1) * 50, (point[0] + 1) * 50) for point in trajectory]
        pygame.draw.lines(screen, BLUE, False, modified_trajectory, 5)


def draw_screen() -> None: # 绘制屏幕
    screen.blit(background_img, dest=(0, 0))
    draw_grid()
    draw_stone()
    if show_button:
        draw_button()

    if game_over.value:
        show_game_over_screen()
        draw_trajectory()

    pygame.display.update()


def retract_chess() -> None: # 悔棋
    cnt = 0
    chessboard = shared_object['value']
    while pos_list and cnt < 2:
        i, j = pos_list.pop()
        chessboard.drop_piece(i, j, Color.BLANK)
        cnt += 1
    shared_object['value'] = chessboard


def show_game_over_screen() -> None: # 提示游戏结束
    if chessboard.is_full():
        message = "The chessboard is full, draw !"
    else:
        winner = 'human' if chessboard.player == Player.AI else 'ai'
        message = f"The game is over! The winner is {winner}!"
    
    font = pygame.font.SysFont(None, 48)
    text = font.render(message, True, BLUE)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text, text_rect)
    #pygame.display.flip()      



# 在进程中操作棋盘对象和AI对象
def ai_task(shared_object:multiprocessing.Manager, 
            pos_list:multiprocessing.Manager, 
            running:multiprocessing.Value, 
            begin_game:multiprocessing.Value,
            game_over:multiprocessing.Value, 
            lock:multiprocessing.Lock,
            depth:int) -> None:
    audio = Audio()
    while running.value:
        if not begin_game.value:
            continue
        chessboard = shared_object['value']
        color = Color.BLACK
        with lock:
            if chessboard.player == Player.HUMAN:
                chessboard.inverse_grid()
                color = Color.WHITE
                
            i, j = Ai(chessboard, depth).get_ai_move()
            print(i, j)
            chessboard.drop_piece(i, j, color)
            if chessboard.is_win(color)[0]:
                game_over.value = 1
            pos_list.append((i, j))

            if chessboard.player == Player.HUMAN:
                chessboard.inverse_grid()
                color = Color.BLACK
                chessboard.player = Player.AI
            else:
                chessboard.player = Player.HUMAN

            shared_object['value'] = chessboard
            audio.audios_dict["drop_piece_sound"].play()
           
# 主函数
if __name__ == '__main__':
    pygame.init()

    # 设置屏幕尺寸和标题
    screen_width, screen_height = 600, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("AI五子棋")

    background_img = pygame.image.load("img/muzm.jpg")
    background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

    # 按钮选项
    button = Button(screen_width, screen_height)

    # 音频
    audio = Audio()

    # 创建一个管理器
    manager = multiprocessing.Manager()

    # 创建一个进程安全的共享对象，并放入棋盘对象
    shared_object = manager.dict()
    shared_object['value'] = Chessboard(11, 11)

    # 创建一个后进先出链表
    pos_list = manager.list()

    running = multiprocessing.Value('i', 1)  # 创建一个共享变量，用于控制任务是否运行
    begin_game = multiprocessing.Value('i', 0)  # 创建一个共享变量，判断游戏是否开始
    game_over = multiprocessing.Value('i', 0) # 创建一个共享变量，判断游戏是否结束

    # 创建一个锁对象
    lock = multiprocessing.Lock()

    # 启动 AI 进程
    ai_process = multiprocessing.Process(target=ai_task, args=(shared_object, pos_list, running, begin_game, game_over, lock, 1))
    ai_process.start()

    ai_process1 = multiprocessing.Process(target=ai_task, args=(shared_object, pos_list, running, begin_game, game_over, lock, 2))
    ai_process1.start()


    show_button = True

    while running.value:
        chessboard = shared_object['value']
        draw_screen()

        if game_over.value or chessboard.is_full():
            chessboard.init()
            del pos_list[:]
            begin_game.value = 0
            show_button = True


        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button != 1:  # 左键
                    continue
                if show_button: # 显示按钮
                    if button.button_dict["start_button"][1].collidepoint(event.pos):
                        begin_game.value = 1
                        show_button = False
                        game_over.value = 0
                        shared_object['value'] = chessboard 
                    elif button.button_dict["quit_button_rect"][1].collidepoint(event.pos):
                        begin_game.value = 0
                        show_button = False
                        running.value = 0
                    elif button.button_dict["retract_button_rect"][1].collidepoint(event.pos):
                        retract_chess()
                        show_button = False
                else:
                    if not begin_game.value:
                        continue

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    begin_game = ~begin_game
                    show_button = ~show_button
            elif event.type == pygame.QUIT:
                running.value = 0  # 设置共享变量为 0，结束 AI 进程

    ai_process.join()  # 等待 AI 进程结束#
    ai_process1.join()


    pygame.quit()
    sys.exit()
