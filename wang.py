#only works for 2 edge wang tileset
# http://www.cr31.co.uk/stagecast/wang/intro.html
# this handles bitwise 2 edge wang tilesets.

import random


def check_wang(value1, value2, side):
    # side is the side of value 1 that is touching value2
    left_side_blue = (0, 1, 2, 3, 4, 5, 6, 7, 16)
    up_side_blue = (0, 2, 4, 6, 8, 10, 12, 14, 16)
    right_side_blue = (0, 1, 4, 5, 8, 9, 12, 13, 16)
    down_side_blue = (0, 1, 2, 3, 8, 9, 10, 11, 16)

    if int(value2) == 16:
        return True
    else:
        if side == 'up':
            if int(value1) in up_side_blue:
                if value2 in down_side_blue:
                    return True
                else:
                    return False
            else: #if not upside blue, up side is yellow
                if value2 not in down_side_blue:
                    return True
                else:
                    return False
        if side == 'down':
            if value1 in down_side_blue:
                if value2 in up_side_blue:
                    return True
                else:
                    return False
            else:
                if value2 not in up_side_blue:
                    return True
                else:
                    return False
        if side == 'left':
            if value1 in left_side_blue:
                if value2 in right_side_blue:
                    return True
                else:
                    return False
            else:
                if value2 not in right_side_blue:
                    return True
                else:
                    return False
        if side == 'right':
            if value1 in right_side_blue:
                if value2 in left_side_blue:
                    return True
                else:
                    return False
            else:
                if value2 not in left_side_blue:
                    return True
                else:
                    return False



def validate_sides(x, y, grid, proposed_value):
    for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # adjacent squares
        checking_position = (x + new_position[0], y + new_position[1])
        side_checked = ''


        if new_position[1] == -1:
            side_checked = 'left'
        elif new_position[1] == 1:
            side_checked = 'right'
        elif new_position[0] == -1:
            side_checked = 'up'
        elif new_position[0] == 1:
            side_checked = 'down'

        if checking_position[0] > (len(grid) - 1) or checking_position[0] < 0 or checking_position[1] > (len(grid[len(grid) - 1]) - 1) or checking_position[1] < 0:
            continue
        else:
            checking = check_wang(proposed_value, grid[checking_position[0]][checking_position[1]], side_checked)
            if checking == False:
                return False
            else:
                continue
    return True


def wang_set(width, height):
    #estabilishes a blank grid separate from the tower grid
    grid = []
    #populates the grid
    for i in range(height):
        grid1 = []
        for j in range(width):
            grid1.append(16)
        grid.append(grid1)
    #randomly select the numerical start value for the first space
    grid[0][0] = random.choice(list(range(0,15)))
    counter = 0
    #loop to propose a value for the next space and validate it as a valid piece
    for i in range(height):
        for j in range(width):
            if i == 0 and j == 0:
                continue
            else:
                acceptable = False
                box_pool = list(range(0, 15))
                while acceptable == False:
                    new_value = random.choice(box_pool)
                    x = validate_sides(i, j, grid, new_value)
                    if x == False:
                        box_pool.remove(new_value)
                    else:
                        box_pool = list(range(0, 15))
                        acceptable = True
                grid[i][j] = new_value
                if new_value == 1 or new_value == 2 or new_value == 4 or new_value == 8:
                    counter += 1
                elif new_value == 3 or new_value == 5 or new_value == 6 or new_value == 9 or new_value == 10 or new_value == 12:
                    counter += 2
                elif new_value == 7 or new_value == 11 or new_value == 13 or new_value == 14:
                    counter += 3
                elif new_value == 15:
                    counter += 4
    if counter * 0.25 >= (12*7) * 0.3:
        return grid
    else:
        wang_set(width, height)
