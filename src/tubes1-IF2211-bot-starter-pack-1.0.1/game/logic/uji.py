import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

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

def avoid_teleport(goal_position, current_position, delta_x, delta_y):
    # (0,0) itu kotak paling kiri atas
    if(delta_x == 0): #pergerakan vertikal
        # berarti bisa digeser kanan atau kiri, tergantung posisi relatif goal terhadap tujuan
        selisih_x = goal_position.x - current_position.x # kalo positif artinya goal ada di sebelah kanan, kita geser ke kanan aja. kalaupun selisihnya nol, kita bebas mau ambil kanan atau kiri
        if(selisih_x>=0):
            return 1, 0
        else:
            return -1,0
    else: # artinya delta_x bergerak ke kanan atau ke kiri, yang mana nilai delta_y pasti 0
        # berarti bisa digeser atas atau bawah, tergantung posisi relatif goal terhadap tujuan
        selisih_y = goal_position.y - current_position.y # kalo positif artinya goal ada di sebelah bawah, kita geser ke bawah aja. kalaupun selisihnya nol, kita bebas mau ambil atas atau bawah
        if(selisih_y>=0):
            return 0, 1
        else:
            return 0,-1

def get_dir(current_position, dest):
    gap_x = abs(dest.x - current_position.x)
    gap_y = abs(dest.y - current_position.y)

    if gap_x >= gap_y : # gerak sumbu x
        if(dest.x - current_position.x >= 0): #dest ada di sebelah kanan
            return(1,0)
        else: #dest ada di sebelah kiri
            return(-1,0)
    else: #gerak sumbu y
        if(dest.y - current_position.y >= 0): #dest ada di sebelah bawah
            return(0,1)
        else: #dest ada di sebelah atas
            return(0,-1)

class Uji(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def next_move(self, board_bot: GameObject, board: Board):
        # inisiasi
        props = board_bot.properties
        current_position = board_bot.position
        teleport_location = [object.position for object in board.game_objects if object.type == "TeleportGameObject"]
        coordinate_and_point, ratio = coordinate_diamond_ratio([coordinate.position for coordinate in board.diamonds], [coordinate.properties.points for coordinate in board.diamonds], current_position)
        goal, is_base = get_coordinate_goal_for_diamond(ratio, coordinate_and_point[0], props.diamonds, coordinate_and_point[1])
        
        print(teleport_location)
        # print(current_position.x, current_position.y)
        # print(ratio)
        # print(coordinate_and_point)
        # print(props.diamonds)
        # print(goal.x, goal.y)

        # Analyze new state
        base = board_bot.properties.base
        if props.diamonds >= 5:
            # Move to base
            self.goal_position = base
        else:
            # Just roam around
            if(not is_base):
                self.goal_position = goal
            else:
                self.goal_position = base


        # We are aiming for a specific position, calculate delta
        delta_x, delta_y = get_direction( current_position.x, current_position.y, self.goal_position.x, self.goal_position.y) # menuju path algo awal
        # delta_x, delta_y = get_dir(current_position, self.goal_position) # enhanced

        # implementasi hindari teleport button
        for tel in teleport_location:
            if((delta_x + current_position.x) == tel.x and (delta_y + current_position.y) == tel.y):
                delta_x, delta_y = avoid_teleport(self.goal_position, current_position, delta_x, delta_y)

            

        return delta_x, delta_y
