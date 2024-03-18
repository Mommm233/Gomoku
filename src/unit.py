# 组件类，显示：时间，步数, play1考虑时长, play2考虑时长
import pygame
pygame.init()

BLACK = (0, 0, 0)

class Unit:
    def __init__(self) -> None:
        self.font = pygame.font.SysFont(None, 22)
        duration_time_text = self.font.render("Time:", True, BLACK)
        step_text = self.font.render("Steps:", True, BLACK)
        human_think_text = self.font.render("Human Think Time:", True, BLACK)
        ai_think_text = self.font.render("AI Think Time:", True, BLACK)
        self.unit_dict = {
            "duration_time": [duration_time_text, duration_time_text.get_rect(center=(50, 10))],
            "step_time": [step_text, step_text.get_rect(center=(150, 10))],
            "human_think_time": [human_think_text, human_think_text.get_rect(center=(300, 10))],
            "ai_think_time": [ai_think_text, ai_think_text.get_rect(center=(500, 10))]
        }

    def update_unit(self, time1:int, num:int, time2:int, time3:int) -> None:
        # 更新时间
        duration_time_message = f"Time: {time1}s" if time1 < 60 else(f"Time: {time1//60}m{time1%60}s" if time1 < 3600 else f"Time: {time1//3600}h{time1//60}m{time1%60}s")
        duration_time_text = self.font.render(duration_time_message, True, BLACK)
        self.unit_dict["duration_time"][0] = duration_time_text
        
        # 更新步数
        step_text = self.font.render(f"Steps: {num}", True, BLACK)
        self.unit_dict["step_time"][0] = step_text
        
        # 更新人类思考时间
        human_think_message = f"Human Think Time: {time2}s" if time2 < 60 else(f"Time: {time2//60}m{time2%60}s" if time2 < 3600 else f"Time: {time2//3600}h{time2//60}m{time2%60}s")
        human_think_text = self.font.render(human_think_message, True, BLACK)
        self.unit_dict["human_think_time"][0] = human_think_text
        
        # 更新AI思考时间
        ai_think_message = f"AI Think Time: {time3}s" if time3 < 60 else(f"Time: {time3//60}m{time3%60}s" if time3 < 3600 else f"Time: {time3//3600}h{time3//60}m{time3%60}s")
        ai_think_text = self.font.render(ai_think_message, True, BLACK)
        self.unit_dict["ai_think_time"][0] = ai_think_text

