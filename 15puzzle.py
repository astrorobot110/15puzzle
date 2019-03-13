# _*_ coding: utf-8 _*_

import os
import random
import copy
import shutil

try:
    from msvcrt import getch
except ImportError:
    def getch():
        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


class Board():
    rightBoard = [[1, 2, 3, 4],
                  [5, 6, 7, 8],
                  [9, 10, 11, 12],
                  [13, 14, 15, 0]]

    direction = {'right': [0, -1],
                 'down': [-1, 0],
                 'up': [1, 0],
                 'left': [0, 1]}

    def __init__(self):
        self.stats = copy.deepcopy(self.rightBoard)
        self.blank = [3, 3]
        self.scramble()

    def __str__(self):
        disp = ['Current board is...', '+---+---+---+---+']

        for idx in range(len(self.stats)):
            statsToDisp = self.__toStrings(self.stats[idx])
            disp.append('|' + '|'.join(list(statsToDisp)) + '|')
            disp.append(disp[1])

        return '\n'.join(disp)

    def scramble(self):
        random.seed()
        direction = ('left', 'down', 'up', 'right')
        for idx in range(100):
            scrambleTo = direction[random.randint(0, 3)]
            self.move(scrambleTo, True)
        return 'done.'

    def __toStrings(self, stats):
        returnTo = []
        for idx in range(len(stats)):
            if stats[idx] > 0:
                returnTo.append(str(stats[idx]).rjust(2) + ' ')
            else:
                returnTo.append('   ')

        return returnTo

    def move(self, direction, *isInit):
        swap = []
        for idx in range(2):
            swap.append(self.blank[idx]+self.direction[direction][idx])

        try:
            if 0 <= swap[0] < 4 and 0 <= swap[1] < 4:
                swapValue = self.stats[swap[0]][swap[1]]
                self.stats[self.blank[0]][self.blank[1]] = swapValue
                self.stats[swap[0]][swap[1]] = 0
            else:
                raise IndexError
        except IndexError:
            if len(isInit) > 0 and isInit[0]:
                returnTo = ''
            else:
                returnTo = 'Can\'t move from out of board.\n'
        else:
            self.blank = copy.copy(swap)
            returnTo = ''
        finally:
            if self.stats == self.rightBoard:
                return 'CONGRATS!'
            else:
                return returnTo


if __name__ == '__main__':
    dirChar = {108: 'left',
               100: 'left',
               107: 'down',
               119: 'down',
               106: 'up',
               115: 'up',
               104: 'right',
               97:  'right'}

    confirm = True
    message = ''
    cls()
    board = Board()
    while confirm:
        print(board, end='\n\n')
        print(message, end='')

        if message != 'CONGRATS!':
            print('Which direction? :')
            direction = ord(getch())
            while True:
                cls()
                try:
                    if direction != 113:
                        message = board.move(dirChar[direction])
                    else:
                        confirm = False
                except KeyError:
                    continue
                finally:
                    break
        else:
            confirm = False
            print('\n\nPush any key to exit.\n')
            getch()
