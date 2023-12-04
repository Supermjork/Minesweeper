# File holding the classes for the Layout
# As well as tiles within

# Tiles to be put within the land
import random


class Tile:
    isMine:   bool = False
    clicked:  bool = False
    surrMines: int = 0

    def __init__(self, mineChance: float = 0.1):
        self.isMine = (random.randrange(0, 100) < mineChance * 100)

    def __str__(self) -> str:
        if self.clicked:
            if self.isMine:
                return "⛝"
            else:
                return "◻"
        else:
            return "◼"
    
    def click(self):
        self.clicked = True

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

    def anyMines(self):
        # iterate over whole board
        # check if all mines are still not clicked
        pass

    def sweep(self):
        over: bool = False

        while(not over):
            coord = tuple(input('Coordinates of Tile (0 Index): ').split())

            tile = self.tiles[int(coord[1])][int(coord[0])]

            tile.click()

            print(self)

            if tile.isMine:
                over = True
                print("Game Over, Stepped on a Mine.")
    
    def __str__(self) -> str:
        return str('\n'.join([' '.join([str(cell) for cell in row]) for row in self.tiles]))

test_board = SweepLand(15, 15, 0.2)

print(test_board)

test_board.sweep()