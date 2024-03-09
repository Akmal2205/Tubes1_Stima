import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction, position_equals

def coordinate_diamond_ratio(coordinates, points, current_position):
    sum_coordinates = [((coordinate.x - current_position.x)**2 + (coordinate.y-current_position.y)**2) for coordinate in coordinates]
    ratio = []

    for i in range (len(sum_coordinates)):
        if (sum_coordinates[i] == 0):
            ratio.append(-1)
        else:
            ratio.append(points[i]/sum_coordinates[i])
    
    return [coordinates, points], ratio

def get_coordinate_goal_for_diamond(list_ratio, list_coordinates, inventory_diamonds, list_point):
    
    # cari index dari nilai max list ratio
    max_ratio = max(list_ratio)
    index = list_ratio.index(max_ratio)

    while(list_point[index]==2 and inventory_diamonds==4):
        list_ratio[index] = -1
        max_ratio = max(list_ratio)
        index = list_ratio.index(max_ratio)

    if(list_ratio[index]==-1):
        return list_coordinates[index], True

    if(inventory_diamonds==4):
        if(list_point[index]==2):
            index-=1

    return list_coordinates[index], False

def red_button(red_pos, curr_pos, diamond_ratio, n_diamond_left):
    distance = ((red_pos.x-curr_pos.x)**2+(red_pos.y-curr_pos.y)**2)
    poin = (2/(distance*n_diamond_left))
    # print("ini point red:", poin)
    if (poin>= max(diamond_ratio)):
        return True
    else:
        return False
    
def teleport_use(diamond_pos, diamond_ratio, teleport2_pos, points):
    _, ratio_teleport = coordinate_diamond_ratio(diamond_pos, points, teleport2_pos)
    # print("ratio", ratio_teleport, diamond_ratio)
    if(max(ratio_teleport)>max(diamond_ratio)):
        return True
    else:
        return False



def avoid_teleport(goal_position, current_position, delta_x, delta_y):
    # (0,0) itu kotak paling kiri atas
    if(delta_x == 0): #pergerakan vertikal
        # berarti bisa digeser kanan atau kiri, tergantung posisi relatif goal terhadap tujuan
        selisih_x = goal_position.x - current_position.x # kalo positif artinya goal ada di sebelah kanan, kita geser ke kanan aja. kalaupun selisihnya nol, kita bebas mau ambil kanan atau kiri
        if(selisih_x>=0 and current_position.x != 14):
            return 1, 0
        else:
            return -1,0
    else: # artinya delta_x bergerak ke kanan atau ke kiri, yang mana nilai delta_y pasti 0
        # berarti bisa digeser atas atau bawah, tergantung posisi relatif goal terhadap tujuan
        selisih_y = goal_position.y - current_position.y # kalo positif artinya goal ada di sebelah bawah, kita geser ke bawah aja. kalaupun selisihnya nol, kita bebas mau ambil atas atau bawah
        if(selisih_y>=0) and current_position.y != 14:
            return 0, 1
        else:
            return 0,-1

def get_dir(current_position, dest):
    gap_x = dest.x - current_position.x
    gap_y = dest.y - current_position.y

    if abs(gap_x) >= abs(gap_y): # gerak sumbu x
        return (1 if gap_x >= 0 else -1, 0)
    else: #gerak sumbu y
        return (0, 1 if gap_y >= 0 else -1)

            
class BotGacor(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
        self.avoid = False
        self.teleport = False

    def next_move(self, board_bot: GameObject, board: Board):
        # inisiasi
        current_position = board_bot.position
        props = board_bot.properties
        if(board_bot.properties.diamonds>=1):
            enemy_location = [(bot.position, bot.properties.name, bot.properties.diamonds) for bot in board.bots if bot.position.x!=current_position.x and bot.position.y!=current_position.y and ((bot.position.x - current_position.x)**2 + (bot.position.y-current_position.y)**2 <=2)]
        else:
            enemy_location = [(bot.position, bot.properties.name, bot.properties.diamonds) for bot in board.bots if bot.position.x!=current_position.x and bot.position.y!=current_position.y and ((bot.position.x - current_position.x)**2 + (bot.position.y-current_position.y)**2 <=2) and bot.properties.diamonds>=2]

        red_pos = [obj.position for obj in board.game_objects if obj.type == "DiamondButtonGameObject"]

        if(len(enemy_location)>0):
            x, y = get_direction(current_position.x, current_position.y, enemy_location[0][0].x, enemy_location[0][0].y)
            return x, y
        
        teleport_location = [object.position for object in board.game_objects if object.type == "TeleportGameObject"]
        # print(current_position.x, current_position.y)
        diamond_pos_in_game = [coordinate.position for coordinate in board.diamonds]
        diamond_point_in_game = [coordinate.properties.points for coordinate in board.diamonds]
        coordinate_and_point, ratio = coordinate_diamond_ratio(diamond_pos_in_game, diamond_point_in_game, current_position)
        goal, is_base = get_coordinate_goal_for_diamond(ratio, coordinate_and_point[0], props.diamonds, coordinate_and_point[1])
        if(red_button(red_pos[0], current_position, ratio, len(diamond_point_in_game))):
            goal = red_pos[0]
        
        # print(teleport_location)

        # Analyze new state
        base = board_bot.properties.base
        if props.diamonds >= 5:
            # Move to base
            self.goal_position = base
        else:
            if(is_base):
                self.goal_position = base
            # Just roam around
            else:
                self.goal_position = goal

        # We are aiming for a specific position, calculate delta

        if(self.avoid):
            delta_x, delta_y = get_dir(current_position, self.goal_position) # enhanced
            self.avoid = False
        else:
            delta_x, delta_y = get_direction( current_position.x, current_position.y, self.goal_position.x, self.goal_position.y) # menuju path algo awal


        # implementasi hindari teleport button
        if(self.teleport==False and props.diamonds<4):
            for tel in teleport_location:           
                if((tel.x-current_position.x)**2+(tel.y-current_position.y)**2 <2):
                    if(teleport_use(diamond_pos_in_game, ratio, (teleport_location[0] if position_equals(teleport_location[1], tel) else teleport_location[1]), diamond_point_in_game) and self.goal_position!=base):
                        delta_x, delta_y = get_direction(current_position.x, current_position.y, tel.x, tel.y)
                        self.teleport = True
                        print(1)
                        break
                    else:
                        if((delta_x + current_position.x) == tel.x and (delta_y + current_position.y) == tel.y):
                            delta_x, delta_y = avoid_teleport(self.goal_position, current_position, delta_x, delta_y)
                            self.avoid = True
                            print(2)
            print(3)
        else:
            self.teleport= False


        return delta_x, delta_y
