# File holding the classes for the Layout
# As well as tiles within

# Tiles to be put within the land
import random

class Tile:
    isMine:   bool = False
    clicked:  bool = False
    flagged:  bool = False
    surrMines: int = 0

    def __init__(self, mineChance: float = 0.1):
        self.isMine = (random.randrange(0, 100) < mineChance * 100)

    def __str__(self) -> str:
        if self.clicked:
            if self.isMine:
                return "⛝"
            else:
                return str(self.surrMines)
        elif self.flagged:
            return "▣"
        else:
            return "◼"
    
    def click(self):
        self.clicked = True
    
    def flag(self):
        self.flagged = True

class SweepLand:
    x: int
    y: int
    tiles: list[list[Tile]]

    def __init__(self, width: int = 1, height: int = 1, chance: float = 0.1):
        self.x = width
        self.y = height
        self.tiles = []

        for _ in range(0, self.y):
            tmp_tiles = []

            for _ in range(0, self.x):
                tmp_tiles.append(Tile(chance))
            
            self.tiles.append(tmp_tiles)

    def getMines(self):
        mineCoordList: list[tuple] = []
        for x in range(self.x):
            for y in range(self.y):
                if self.tiles[x][y].isMine == True:
                    mineCoordList.append((x, y))
        
        return mineCoordList
    
    def valid(self, x, y):
        return (0 <= x < self.x) and (0 <= y < self.y)
    
    def proxMines(self):
        mineList = self.getMines()

        for mine in mineList:
            # Setting Mine Directions
            dirs = ['N', 'S', 'E', 'W', 'NE', 'NW', 'SE', 'SW']

            for dir in dirs:
                if dir == 'N':
                    if self.valid(mine[0], mine[1] - 1):
                        self.tiles[mine[0]][mine[1] - 1].surrMines += 1

                if dir == 'S':
                    if self.valid(mine[0], mine[1] + 1):
                        self.tiles[mine[0]][mine[1] + 1].surrMines += 1

                if dir == 'E':
                    if self.valid(mine[0] + 1, mine[1]):
                        self.tiles[mine[0] + 1][mine[1]].surrMines += 1

                if dir == 'W':
                    if self.valid(mine[0] - 1, mine[1]):
                        self.tiles[mine[0] - 1][mine[1]].surrMines += 1

                if dir == 'NE':
                    if self.valid(mine[0] + 1, mine[1] - 1):
                        self.tiles[mine[0] + 1][mine[1] - 1].surrMines += 1

                if dir == 'NW':
                    if self.valid(mine[0] - 1, mine[1] - 1):
                        self.tiles[mine[0] - 1][mine[1] - 1].surrMines += 1

                if dir == 'SW':
                    if self.valid(mine[0] - 1, mine[1] + 1):
                        self.tiles[mine[0] - 1][mine[1] + 1].surrMines += 1

                if dir == 'SE':
                    if self.valid(mine[0] + 1, mine[1] + 1):
                        self.tiles[mine[0] + 1][mine[1] + 1].surrMines += 1

    def sweep(self):
        over: bool = False
        flagged: set = set()
        mines: set = self.getMines()

        self.proxMines()

        while(not over):
            coord = tuple(input('Coordinates of Tile (0 Index) and state (C or F): ').split())

            tile = self.tiles[int(coord[0])][int(coord[1])]

            if coord[2] == 'C':
                tile.click()

                if tile.isMine:
                    over = True
                    print("Game Over, Stepped on a Mine.")
            elif coord[2] == 'F':
                tile.flag()
                flagged.add((int(coord[0]), int(coord[1])))

            print(self)

            if set(mines) == set(flagged):
                over = True
                print("GG, Game over and you've won.")
            
    
    def __str__(self) -> str:
        return str('\n'.join([' '.join([str(cell) for cell in row]) for row in self.tiles]))

test_board = SweepLand(2, 2, 1)

print(test_board)

test_board.sweep()
