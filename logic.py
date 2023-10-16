import numpy as np
import random
import math


class Field:
    def __init__(self, width, height, wall):
        self.field = np.zeros([height, width], dtype=int)
        self.width = width
        self.height = height
        self.wall = wall
        self.step = 0

    def __repr__(self):
        output = ""

        shift = math.ceil(len(str(self.step))/2)

        output += "-"
        for i in range(self.width - shift):
            output += "-"
        output += str(self.step)
        for i in range(self.width - shift):
            output += "-"
        if len(str(self.step))%2 == 1:
            output += "-"

        output += "\n"

        for line in self.field:
            x = 0
            output += "|"

            for val in line:
                x += 1

                if val == 1:
                    output += "@"
                else:
                    output += " "

                if x < self.width:
                    output += " "

            output += "|"
            output += "\n"

        for i in range(2*self.width):
            output += "-"

        return output

    def set(self, x, y):
        self.field[y][x] = 1

    def unset(self, x, y):
        self.field[y][x] = 0

    def random_set(self):
        for y in range(self.height):
            for x in range(self.width):
                self.field[y][x] = random.randint(0, 1)

    def reset(self, width, height, wall):
        self.field = np.zeros([height, width], dtype=int)
        self.width = width
        self.height = height
        self.wall = wall
        self.step = 0

    def update(self):
        self.step += 1

        tmp = np.zeros([self.height, self.width], dtype=int)

        for y in range(self.height):
            for x in range(self.width):
                sum = 0

                if self.wall:
                    if (x - 1 != -1) and (y - 1 != -1):
                        sum += self.field[y-1][x-1]
                    if x - 1 != -1:
                        sum += self.field[y][x-1]
                    if (x - 1 != -1) and (y + 1 != self.height):
                        sum += self.field[y+1][x-1]
                    if y - 1 != -1:
                        sum += self.field[y-1][x]
                    if y + 1 != self.height:
                        sum += self.field[y+1][x]
                    if (x + 1 != self.width) and (y - 1 != -1):
                        sum += self.field[y-1][x+1]
                    if x + 1 != self.width:
                        sum += self.field[y][x+1]
                    if (x + 1 != self.width) and (y + 1 != self.height):
                        sum += self.field[y+1][x+1]
                else:
                    if x-1 == -1:
                        x_minus_one = self.width-1
                    else:
                        x_minus_one = x - 1

                    if x+1 == self.width:
                        x_plus_one = 0
                    else:
                        x_plus_one = x + 1

                    if y - 1 == -1:
                        y_minus_one = self.height - 1
                    else:
                        y_minus_one = y - 1

                    if y + 1 == self.height:
                        y_plus_one = 0
                    else:
                        y_plus_one = y + 1

                    sum += self.field[y_minus_one][x_minus_one]
                    sum += self.field[y][x_minus_one]
                    sum += self.field[y_plus_one][x_minus_one]
                    sum += self.field[y_minus_one][x]
                    sum += self.field[y_plus_one][x]
                    sum += self.field[y_minus_one][x_plus_one]
                    sum += self.field[y][x_plus_one]
                    sum += self.field[y_plus_one][x_plus_one]


                if sum == 2:
                    tmp[y][x] = self.field[y][x]
                elif sum == 3:
                    tmp[y][x] = 1
                else:
                    tmp[y][x] = 0

        self.copy_field(tmp)

    def copy_field(self, field):
        self.field = field.copy()