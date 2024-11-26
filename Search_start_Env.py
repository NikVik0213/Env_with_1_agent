import time
from collections import deque
import pygame
import gymnasium as gym
import numpy as np
import random
import math
import const

clock = pygame.time.Clock()
Flower_LEN_GOAL = 30


def collision_with_flower(flower_position, score):
    flower_position = [random.randrange(1,50)*10,random.randrange(1,50)*10]
    score += 5
    return flower_position, score

def collision_with_base(base_position, score):
    base_position = [250,250]
    score += 1
    return base_position, score

def collision_with_difficult(difficult_position, score):
    difficult_position = [random.randrange(1,50)*10,random.randrange(1,50)*10]
    score -= 5
    return difficult_position, score



def collision_with_boundaries(dron):
    if dron[0]>=500 or dron[0]<0 or dron[1]>=500 or dron[1]<0 :
        return 1
    else:
        return 0

class SearchEnv(gym.Env):
    def __init__(self):
        super(SearchEnv, self).__init__()
        pygame.init()
        
        
        FOG_COLOR = (0, 0, 0)

        #self.grid_size = const.GRID_SIZE
        self.screen = pygame.display.set_mode((550, 670))
        self.clock = pygame.time.Clock()
        self.list_flowers = []

        self.fog_layer = pygame.Surface((550, 670))
        self.fog_layer.fill(FOG_COLOR)
        self.fog_layer.set_alpha(180)
        
        self.dron_vis_rad = 75
        self.screen.fill(const.GREEN)
        self.screen.blit(self.fog_layer, (0, 0))
        self.is_search_area = 0

        

        self.action_space = gym.spaces.Discrete(4)
        self.observation_space = gym.spaces.Box(
            low=-500,
            high=500,
            shape=(36,),
            dtype=np.float64
        )

    # def reset_objects_positions(self):
    #     """
    #     Reset positions of objects
    #     :return: function for get object's postitions
    #     """
    #     if const.PLACEMENT_MODE == 'random':
    #         self._randomize_positions()
    #     elif const.PLACEMENT_MODE == 'fixed':
    #         self._fixed_positions()
    #     else:
    #         raise ValueError("Invalid PLACEMENT_MODE. Choose 'random' or 'fixed'.")

    # def _randomize_positions(self):
    #     """
    #     Get random positions of objects
    #     """
    #     unavailable_positions = {self.base_position}
    #     self.target_positions = self._get_objects_positions(unavailable_positions, const.COUNT_FLOWERS)
    #     unavailable_positions.update(self.target_positions)
    #     self.hole_positions = self._get_objects_positions(unavailable_positions, const.COUNT_HOLES)

    # def _fixed_positions(self):
    #     """
    #     Get fixed positions of objects
    #     """
    #     self.target_positions = const.FIXED_FLOWER_POSITIONS.copy()
    #     self.hole_positions = const.FIXED_HOLE_POSITIONS.copy()

    # def _get_available_positions(self, unavailable: set) -> list:
    #     """
    #     Function for get available positions from all positions - unavailable
    #     :param unavailable: set
    #     :return: available positions
    #     """
    #     all_positions = [(i, j) for i in range(self.grid_size) for j in range(self.grid_size)]
    #     return [pos for pos in all_positions if pos not in unavailable]

    # def _get_objects_positions(self, unavailable: (), size: int) -> list:
    #     """
    #     Get list of object's positions using unavailable positions
    #     :param unavailable: set()
    #     :param size: int
    #     :return: list of positions [x, y]
    #     """
    #     available_positions = self._get_available_positions(unavailable)
    #     indices = np.random.choice(len(available_positions), size=size, replace=False)
    #     return [available_positions[i] for i in indices]

    def reset(self, *, seed=None, options=None):
        self.screen.fill(const.GREEN)
        self.screen.blit(self.fog_layer, (0, 0))
        self.is_search_area = 0
        #self.screen.fill(const.GREEN)
        #self.img = np.zeros((500,500,3),dtype='uint8')
        self.charge_time = time.time()
        self.start_time = time.time()
        self.base_position = [250,250]
        self.dron_position = [[250,250],[240,250],[230,250]]
        self.flower_position = [random.randrange(1,50)*10,random.randrange(1,50)*10]
        #self.difficult_position = [random.randrange(1,50)*10,random.randrange(1,50)*10]
        self.score = 0
        self.prev_button_direction = 1
        self.button_direction = 1
        self.dron = [250,250]
        self.dron_vis_rad = 75
        self.list_flowers = []
        Energy = 100

        self.prev_reward = 0

        self.done = False

        dron_x = self.dron[0]
        dron_y = self.dron[1]

        flower_delta_x = self.flower_position[0] - dron_x
        flower_delta_y = self.flower_position[1] - dron_y

        #difficult_delta_x = self.difficult_position[0] - dron_x
        #difficult_delta_y = self.difficult_position[1] - dron_y

        # base_delta_x = self.base_position[0] - dron_x
        # base_delta_y = self.base_position[1] - dron_y

        self.prev_actions = deque(maxlen = Flower_LEN_GOAL)  # 
        for i in range(Flower_LEN_GOAL):
            self.prev_actions.append(-1) # to create history

        # create observation:
        observation = [dron_x, dron_y, flower_delta_x, flower_delta_y,Energy,self.is_search_area] + list(self.prev_actions)
        observation = np.array(observation)
        info = {}

        return observation,info
        # self.reset_objects_positions()
        # self.agent_position = self.base_position
        # self.watered_status = np.zeros(const.COUNT_FLOWERS)
        # self.water_tank = const.WATER_CAPACITY
        # self.energy = const.ENERGY_CAPACITY
        # self.visited = np.zeros((self.grid_size, self.grid_size), dtype=int)
        # self.start_time = time.time()
        # self.reward = 0
        # self.step_count = 0
        # self.position_history = deque(maxlen=10)
        # self.action_history = deque(maxlen=5)
        # self.action_history.clear()
        # self.known_holes = set()
        # self.known_flowers = set()
        # self.explored_cells = set()
        # #logging.info("Environment reset")
        # obs = self._get_observation()
        # if obs.shape != self.observation_space.shape:
        #     raise ValueError(
        #         f"Observation shape {obs.shape} does not match observation_space {self.observation_space.shape}"
        #     )
        # return obs, {}

    # def _get_observation(self):
    #     visible_area = []
    #     for dx in range(-const.VIEW_RANGE, const.VIEW_RANGE + 1):
    #         for dy in range(-const.VIEW_RANGE, const.VIEW_RANGE + 1):
    #             x, y = self.agent_position[0] + dx, self.agent_position[1] + dy
    #             if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
    #                 pos = (x, y)
    #                 if pos in self.hole_positions:
    #                     visible_area.extend([1, 0])  # Яма
    #                     if pos not in self.known_holes:
    #                         self.known_holes.add(pos)
    #                         logging.debug(f"Новая известная яма: {pos}")
    #                 elif pos in self.target_positions:
    #                     idx = self.target_positions.index(pos)
    #                     watered = self.watered_status[idx]
    #                     visible_area.extend([2, watered])  # Цветок
    #                     if pos not in self.known_flowers:
    #                         self.known_flowers.add(pos)
    #                         logging.debug(f"Новый известный цветок: {pos}")
    #                 else:
    #                     visible_area.extend([0, 0])  # Пустая клетка
    #                 self.explored_cells.add(pos)
    #             else:
    #                 visible_area.extend([-1, 0])  # Вне границ

    #     observation = np.concatenate([
    #         np.array(self.agent_position, dtype=float),  # 0-1
    #         np.array([self.water_tank, self.energy], dtype=float),  # 2-3
    #         np.array(visible_area, dtype=float),  # 4-21
    #     ])  # Всего 22 элемента
    #     if observation.shape != self.observation_space.shape:
    #         raise ValueError(
    #             f"Observation shape {observation.shape} does not match observation_space {self.observation_space.shape}"
    #         )
    #     return observation

    def step(self, action):
        self.prev_actions.append(action)
        
        Time_from_charge = time.time() - self.charge_time
        elapsed_time = time.time() - self.start_time  # Рассчитываем время
        font = pygame.font.SysFont(None, const.FONT_SIZE)
        Energy = (1 - Time_from_charge/60)*100
        

        

        
        button_direction = action
        if button_direction == 1:
            self.dron[0] += 10
            
        elif button_direction == 0:
            self.dron[0] -= 10
            
        elif button_direction == 2:
            self.dron[1] += 10
            
        elif button_direction == 3:
            self.dron[1] -= 10

        
        #self.screen.fill((0, 0, 0))
        energy_reward = 0
        flower_reward = 0
        search_reward = 0
        

        
        vision_circle = pygame.Surface((self.dron_vis_rad * 2, self.dron_vis_rad * 2), pygame.SRCALPHA)
        pygame.draw.circle(vision_circle, const.GREEN, (self.dron_vis_rad, self.dron_vis_rad), self.dron_vis_rad)
        self.screen.blit(vision_circle, (self.dron[1] - self.dron_vis_rad + const.CELL_SIZE/2, self.dron[0] - self.dron_vis_rad + const.CELL_SIZE/2))
        # Отрисовка агента
        self.screen.blit(const.AGENT_ICON, (self.dron[1],
                                            self.dron[0]))
        
        flower = (self.flower_position[1],self.flower_position[0])
        
        euclidean_dist_to_flower = np.linalg.norm(np.array(self.dron) - np.array(self.flower_position))
        dist = math.hypot(self.flower_position[0] - self.dron[0], self.flower_position[1] - self.dron[1])
        if dist < self.dron_vis_rad and flower not in self.list_flowers:
            self.list_flowers.append(flower)
            flower_reward = 1000
        #self.screen.blit(const.HOLE_ICON, (self.difficult_position[1], self.difficult_position[0]))
        self.screen.blit(const.BASE_ICON, (self.base_position[1], self.base_position[0]))
        

        for flowers in self.list_flowers:
            self.screen.blit(const.FLOWER_ICON, (flowers[0], flowers[1]))


        if self.is_search_area > 4 and self.is_search_area < 5:
            search_reward += 50
        if self.is_search_area > 9 and self.is_search_area < 10:
            search_reward += 100  
        if self.is_search_area > 14 and self.is_search_area < 15:
            search_reward += 150
        if self.is_search_area > 24 and self.is_search_area < 25:
            search_reward += 250    
        if self.is_search_area > 49 and self.is_search_area < 50:
            search_reward += 500
        if self.is_search_area > 74 and self.is_search_area < 75:
            search_reward += 750
        if self.is_search_area > 94 and self.is_search_area < 95:
            search_reward += 1000       
        
        """ if self.dron == self.flower_position:
            self.flower_position, self.score = collision_with_flower(self.flower_position, self.score)
            flower_reward = 10000 """
        
        if collision_with_boundaries(self.dron) == 1 :
            font = pygame.font.SysFont(None, const.FONT_SIZE)
            message = f"Конец игры, награда: {int(self.score)}"
            text_surface = font.render(message,False,(255,255,255))
            self.screen.blit(text_surface, (0,0))
            self.done = True
        
        # if  Energy < 1:
        #     #difficult_reward = 10000
        #     font = pygame.font.SysFont(None, const.FONT_SIZE)
        #     message = f"Конец игры, награда: {int(self.score)}"
        #     text_surface = font.render(message,False,(255,255,255))
        #     self.screen.blit(text_surface, (0,0))
        #     self.done = True
        
        if Energy <= 35:
            energy_reward -= 100


        # if self.dron == self.base_position:
        #     self.charge_time = time.time()
        #     self.base_position, self.score = collision_with_base(self.flower_position, self.score)
        #     energy_reward += 300

        


        if self.is_search_area < 95:
            search_reward -=10
        #euclidean_dist_to_difficult = np.linalg.norm(np.array(self.dron) - np.array(self.difficult_position))
        self.total_reward = ((1000 - ((100-self.is_search_area)*10)) + flower_reward + energy_reward + search_reward )/100
        




        self.reward = self.total_reward - self.prev_reward
        self.prev_reward = self.total_reward

        if self.done:
            self.reward = -1000
        info = {}


        dron_x = self.dron[0]
        dron_y = self.dron[1]

        flower_delta_x = self.flower_position[0] - dron_x
        flower_delta_y = self.flower_position[1] - dron_y

       # difficult_delta_x = self.difficult_position[0] - dron_x
       # difficult_delta_y = self.difficult_position[1] - dron_y

        #base_delta_x = self.base_position[0] - dron_x
        #base_delta_y = self.base_position[1] - dron_y

        # create observation:

        observation = [dron_x, dron_y, flower_delta_x, flower_delta_y,Energy,self.is_search_area] + list(self.prev_actions)
        observation = np.array(observation)
        

        status_bar_height = 120  # Высота панели статуса
        status_bar_rect = pygame.Rect(0, 550, 550,
                                      status_bar_height)  # Прямоугольник для панели статуса
        pygame.draw.rect(self.screen, const.WHITE, status_bar_rect)

        self.screen.blit(font.render(f"Время: {elapsed_time:.2f} сек", True, const.BLACK),
                         (10, 550 + 10))
        self.screen.blit(font.render(f"Очки: {int(self.score)}", True, const.BLACK),
                          (10, 550 + 40))
        self.screen.blit(font.render(f"Энергия: {int(Energy)}", True, const.BLACK),
                          (10, 550 + 70))
        self.screen.blit(font.render(f"Исследованная площадь: {self.is_search_area}", True, const.BLACK),
                          (10, const.SCREEN_SIZE + 100))
        # self.screen.blit(font.render(f"Вода: {self.water_tank}", True, const.BLACK),
        #                  (200, const.SCREEN_SIZE + 40))
        # self.screen.blit(font.render(f"Шаги: {self.step_count}", True, const.BLACK),
        #                  (400, const.SCREEN_SIZE + 10))
        # self.screen.blit(font.render(f"Обнаружено ям: {len(self.known_holes)}/{const.COUNT_HOLES}",
        #                              True, const.BLACK), (400, const.SCREEN_SIZE + 40))
        # self.screen.blit(
        #     font.render(f"Обнаружено цветков: {len(self.Flower_LEN_GOAL)}",
        #                 True, const.BLACK), (10, const.SCREEN_SIZE + 70))
        # self.screen.blit(font.render(f"Полито цветков: {int(np.sum(self.watered_status))}/"
        #                              f"{const.COUNT_FLOWERS}", True, const.BLACK), (300, const.SCREEN_SIZE + 70))
        
        
        pygame.display.flip()
        #pygame.time.wait(5)
        #pygame.display.update()
        self.clock.tick(60)
        pixel_array = pygame.surfarray.array3d(self.screen)
        is_target_color = np.all(pixel_array == const.GREEN, axis=-1)
        count = np.sum(is_target_color)
        self.is_search_area = 100/(500*600)*count 

        return observation, self.total_reward,False, self.done, info
pygame.quit()





       
        # # Определяем известные неполитые цветки


        # # Действия агента в зависимости от выбранного действия
        # match action:
        #     case 0:  # Вверх
        #         new_position = (max(0, self.agent_position[0] - 1), self.agent_position[1])
        #         self.energy -= const.ENERGY_CONSUMPTION_MOVE
        #     case 1:  # Вниз
        #         new_position = (min(self.grid_size - 1, self.agent_position[0] + 1), self.agent_position[1])
        #         self.energy -= const.ENERGY_CONSUMPTION_MOVE
        #     case 2:  # Влево
        #         new_position = (self.agent_position[0], max(0, self.agent_position[1] - 1))
        #         self.energy -= const.ENERGY_CONSUMPTION_MOVE
        #     case 3:  # Вправо
        #         new_position = (self.agent_position[0], min(self.grid_size - 1, self.agent_position[1] + 1))
        #         self.energy -= const.ENERGY_CONSUMPTION_MOVE
        #     case 4:  # Полив
        #         self.water_tank -= const.WATER_CONSUMPTION
        #         self.energy -= const.ENERGY_CONSUMPTION_WATER
        #         if self.action_history[0] == 5:
        #             logging.info('Aгент попытался полить тоже место второй раз подряд ')
        #             self.reward += const.PENALTY_WATER_FAIL_NOT_ON_FLOWER * 2
        #         elif self.agent_position in self.target_positions:
        #             logging.info(f"Полил цветок на позиции {self.agent_position}")
        #             idx = self.target_positions.index(self.agent_position)
        #             if self.watered_status[idx] == 0:
        #                 self.watered_status[idx] = 1
        #                 if self.agent_position in known_unwatered_flowers:
        #                     self.reward += const.REWARD_WATER_KNOWN_FLOWER
        #                 else:
        #                     self.reward += const.REWARD_WATER_SUCCESS
        #             else:
        #                 self.reward += const.PENALTY_WATER_FAIL_ALREADY_WATERED
        #                 logging.warning(
        #                     f"Агент попытался полить цветок, который уже полит")
        #         else:
        #             self.reward += const.PENALTY_WATER_FAIL_NOT_ON_FLOWER
        #             logging.warning(f"Агент попытался полить вне цветка")
        #         new_position = self.agent_position

        #     case _:
        #         new_position = self.agent_position

        # # Запись истории позиций для обнаружения циклов
        # # если в последних 10 записях повторяется 3 раза позиция
        # self.position_history.append(new_position)
        # if self.position_history.count(new_position) > 3 and action != 4:
        #     self.reward += const.PENALTY_LOOP
        #     logging.info('Penalty')

        # # если был на цветке на прошлом шаге и на этом не поливает
        # prev_position = ([obs[0], obs[1]])
        # if (prev_position in known_unwatered_flowers) and (action != 5) == 0:
        #     self.reward += const.DONT_WATERING
        #     logging.info(
        #         f"Должен был поливать цветок на {prev_position}, но выбрал иное действие {action}")

        # # Проверяем, не в яме ли агент
        # self.is_in_hole(new_position)

        # # Обновление посещенных клеток - пределы поля учитывать
        # self.update_visited_cells(new_position)

        # # Проверка на завершение
        # terminated = False
        # truncated = False
        # info = {}

        # if np.all(self.watered_status == 1):
        #     logging.info("Все цветы политы")
        #     self.agent_position = self.base_position
        #     logging.info("Агент вернулся на базу")
        #     # условие по времени выполнения
        #     if self.step_count <= const.MIN_GAME_STEPS:
        #         self.reward += const.REWARD_COMPLETION * 3
        #     else:
        #         self.reward += const.REWARD_COMPLETION
        #     terminated = True

        # if self.step_count >= const.MAX_STEPS_GAME:  # костыль чтоб не циклился
        #     logging.info("Достигнуто максимальное количество шагов")
        #     truncated = True

        # self.agent_position = new_position
        # obs = self._get_observation()
        # logging.info(
        #     f"Шаг: {self.step_count},"
        #     f"Действие: {action} - {self.agent_position}, "
        #     f"Награда: {self.reward}, "
        #     f"Завершено: {terminated}, "
        #     f"Прервано: {truncated}"
        # )
        # return obs, self.reward, terminated, truncated, info

    # def is_in_hole(self, new_position):
    #     """Is agent in hole, reward depends of knowmed hole or not"""
    #     if new_position in self.hole_positions:
    #         if new_position in self.known_holes:
    #             self.reward += const.PENALTY_COLLISION * 2
    #             logging.warning(f"Агент попытался зайти в известную яму на позиции {new_position}")
    #         else:
    #             self.reward += const.PENALTY_COLLISION
    #             logging.warning(f"Агент попал в неизвестную яму на позиции {new_position}")
    #             self.agent_position = new_position
    #             self.known_holes.add(new_position)

    # def get_unwatered_flowers(self) -> list[tuple]:
    #     """Return list of coordinates of unwatered flowers"""
    #     return [
    #         pos for idx, pos in enumerate(self.target_positions)
    #         if self.watered_status[idx] == 0 and pos in self.known_flowers
    #     ]

    # def update_visited_cells(self, new_position):
    #     """Update visited and explored cells"""
    #     if self.visited[new_position] == 0:
    #         self.visited[new_position] = 1
    #     if new_position not in self.explored_cells:
    #         self.reward += const.REWARD_EXPLORE
    #         self.explored_cells.add(new_position)

    # def render(self):
    #     """Render agent game"""
    #     self.screen.fill(const.GREEN)
    #     # Отрисовка сетки
    #     for x in range(self.grid_size):
    #         for y in range(self.grid_size):
    #             pygame.draw.rect(self.screen, const.BLACK,
    #                              (x * const.CELL_SIZE, y * const.CELL_SIZE, const.CELL_SIZE, const.CELL_SIZE),
    #                              1)  # Рисуем черную границу вокруг каждой клетки

    #     # Отрисовка базы
    #     self.screen.blit(const.BASE_ICON,
    #                      (self.base_position[1] * const.CELL_SIZE, self.base_position[0] * const.CELL_SIZE))

    #     # Рисуем цветы и ямы, которые были обнаружены
    #     for i, pos in enumerate(self.target_positions):
    #         if pos in self.known_flowers:
    #             if self.watered_status[i]:
    #                 icon = const.WATERED_FLOWER_ICON
    #             else:
    #                 icon = const.FLOWER_ICON
    #             self.screen.blit(icon, (pos[1] * const.CELL_SIZE, pos[0] * const.CELL_SIZE))

    #     for hole in self.hole_positions:
    #         if hole in self.known_holes:
    #             self.screen.blit(const.HOLE_ICON, (hole[1] * const.CELL_SIZE, hole[0] * const.CELL_SIZE))

    #     # Накладываем исследование области
    #     for x in range(self.grid_size):
    #         for y in range(self.grid_size):
    #             pos = (x, y)
    #             if pos not in self.explored_cells:
    #                 dark_overlay = pygame.Surface((const.CELL_SIZE, const.CELL_SIZE), pygame.SRCALPHA)
    #                 dark_overlay.fill((0, 0, 0, 200))  # Непрозрачный
    #                 self.screen.blit(dark_overlay, (y * const.CELL_SIZE, x * const.CELL_SIZE))

    #     # Отрисовка времени, очков, заряда и уровня воды
    #     elapsed_time = time.time() - self.start_time  # Рассчитываем время
    #     font = pygame.font.SysFont(None, const.FONT_SIZE)
    #     status_bar_height = 120  # Высота панели статуса
    #     status_bar_rect = pygame.Rect(0, const.SCREEN_SIZE, const.SCREEN_SIZE,
    #                                   status_bar_height)  # Прямоугольник для панели статуса
    #     pygame.draw.rect(self.screen, const.WHITE, status_bar_rect)

    #     self.screen.blit(font.render(f"Время: {elapsed_time:.2f} сек", True, const.BLACK),
    #                      (10, const.SCREEN_SIZE + 10))
    #     self.screen.blit(font.render(f"Очки: {int(self.reward)}", True, const.BLACK),
    #                      (10, const.SCREEN_SIZE + 40))
    #     self.screen.blit(font.render(f"Энергия: {self.energy}", True, const.BLACK),
    #                      (200, const.SCREEN_SIZE + 10))
    #     self.screen.blit(font.render(f"Вода: {self.water_tank}", True, const.BLACK),
    #                      (200, const.SCREEN_SIZE + 40))
    #     self.screen.blit(font.render(f"Шаги: {self.step_count}", True, const.BLACK),
    #                      (400, const.SCREEN_SIZE + 10))
    #     self.screen.blit(font.render(f"Обнаружено ям: {len(self.known_holes)}/{const.COUNT_HOLES}",
    #                                  True, const.BLACK), (400, const.SCREEN_SIZE + 40))
    #     self.screen.blit(
    #         font.render(f"Обнаружено цветков: {len(self.known_flowers)}/{const.COUNT_FLOWERS}",
    #                     True, const.BLACK), (10, const.SCREEN_SIZE + 70))
    #     self.screen.blit(font.render(f"Полито цветков: {int(np.sum(self.watered_status))}/"
    #                                  f"{const.COUNT_FLOWERS}", True, const.BLACK), (300, const.SCREEN_SIZE + 70))

    #     # Отрисовка агента
    #     self.screen.blit(const.AGENT_ICON, (self.agent_position[1] * const.CELL_SIZE,
    #                                         self.agent_position[0] * const.CELL_SIZE))

    #     pygame.display.flip()
    #     pygame.time.wait(10)

    # def render_message(self, render_text: str):
    #     """
    #     Display message in the center of screen
    #     :param render_text: str
    #     :return:
    #     """
    #     self.screen.fill(const.BLACK)
    #     text_surf = pygame.font.SysFont(None, const.TITLE_SIZE).render(render_text, True, const.GREEN)
    #     self.screen.blit(text_surf, text_surf.get_rect(center=(const.SCREEN_SIZE // 2, const.SCREEN_SIZE // 2)))
    #     pygame.display.flip()
