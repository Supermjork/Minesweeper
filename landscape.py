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
        mineCoordList: set = set()
        emptyCoordList: set = set()
        for x in range(self.x):
            for y in range(self.y):
                if self.tiles[x][y].isMine == True:
                    mineCoordList.add((x, y))
                else:
                    emptyCoordList.add((x, y))
        
        return mineCoordList, emptyCoordList
    
    def valid(self, x, y):
        return (0 <= x < self.x) and (0 <= y < self.y)
    
    def proxMines(self):
        mineList = self.getMines()[0]

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
        mines, empty = self.getMines()
        empty_compare: set = set()

        self.proxMines()

        while(not over):
            coord = tuple(input('Coordinates of Tile (0 Index) and state (C or F): ').split())

            tile = self.tiles[int(coord[0])][int(coord[1])]

            if coord[2].lower() == 'c':
                tile.click()
                empty_compare.add((int(coord[0]), int(coord[1])))

                if tile.isMine:
                    over = True
                    print("Game Over, Stepped on a Mine.")
            elif coord[2].lower() == 'f':
                tile.flag()
                flagged.add((int(coord[0]), int(coord[1])))

            print(self)

            if (set(mines) == set(flagged)) and (set(empty) == set(empty_compare)) :
                over = True
                print("GG, Game over and you've won.")
            
    
    def __str__(self) -> str:
        return str('\n'.join([' '.join([str(cell) for cell in row]) for row in self.tiles]))

    def dfs(self, x, y):
        if not self.valid(x, y) or self.tiles[x][y].clicked or self.tiles[x][y].flagged:
            return

        self.tiles[x][y].click()

        if self.tiles[x][y].surrMines == 0:
            # Recursive DFS for neighboring tiles
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx, ny = x + dx, y + dy
                    if self.valid(nx, ny):
                        self.dfs(nx, ny)

    def solve(self):
        over = False
        mines, empty = self.getMines()
        flagged = set()

        self.proxMines()

        while not over:
            updated = False

            for x in range(self.x):
                for y in range(self.y):
                    tile = self.tiles[x][y]

                    if not tile.clicked and not tile.flagged:
                        if tile.isMine:
                            print(f"Stepped on a Mine at ({x}, {y}). Returning to previous state.")
                        else:
                            self.dfs(x, y)
                            updated = True

                        if tile.isMine and not tile.flagged:
                            tile.flag()
                            flagged.add((x, y))

            print(self)

            if set(mines) == set(flagged) and set(empty) == set(self.getMines()[1]):
                over = True
                print("GG, you've won.")
            
            if not updated:
                # No updates were made, and the game is not over
                print("Solver cannot make progress. The puzzle may be unsolvable.")


test_board = SweepLand(6, 6, 0.1)

test_board.solve()
