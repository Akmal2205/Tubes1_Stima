import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

def coordinate_diamond_ratio(coordinates, points, current_position):
    sum_coordinates = [((point.x - current_position.x)**2 + (point.y-current_position.y)**2) for point in coordinates]
    ratio = []

    for i in range (len(sum_coordinates)):
        if (sum_coordinates == 0):
            ratio.append(-1)
        else:
            ratio.append(points[i]/sum_coordinates[i])
    
    return [coordinates, points], ratio

def get_coordinate_goal_for_diamond(list_ratio, list_coordinates):
    # cari index dari nilai max list ratio
    max_ratio = max(list_ratio)
    index = list_ratio.index(max_ratio)

    return list_coordinates[index]

class BotGacor(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        current_position = board_bot.position
        print(current_position.x, current_position.y)
        coordinate_and_point, ratio = coordinate_diamond_ratio([coordinate.position for coordinate in board.diamonds], [coordinate.properties.points for coordinate in board.diamonds], current_position)
        print(ratio)
        print(coordinate_and_point)
        goal = get_coordinate_goal_for_diamond(ratio, coordinate_and_point[0])
        print(goal.x, goal.y)

        # Analyze new state
        if props.diamonds == 5:
            # Move to base
            base = board_bot.properties.base
            self.goal_position = base
        else:
            # Just roam around
            self.goal_position = goal

        if self.goal_position:
            # We are aiming for a specific position, calculate delta
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
        else:
            # Roam around
            delta = self.directions[self.current_direction]
            delta_x = delta[0]
            delta_y = delta[1]
            if random.random() > 0.6:
                self.current_direction = (self.current_direction + 1) % len(
                    self.directions
                )
        
        print (delta_x, delta_y)
        return delta_x, delta_y
