import pygame


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cellSize = 30
        self.turn = "cross"
        self.indentation = 3

    def set_view(self, left, top, cellSize):
        self.left = left
        self.top = top
        self.cellSize = cellSize

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, (0, 0, 0), (
                    self.left + self.cellSize * j, self.top + self.cellSize * i, self.cellSize, self.cellSize),
                                 width=0)
                pygame.draw.rect(screen, (255, 255, 255), (
                    self.left + self.cellSize * j, self.top + self.cellSize * i, self.cellSize, self.cellSize),
                                 width=1)
                if self.board[i][j] == 1:
                    pygame.draw.line(screen, (0, 0, 255), (
                        self.left + self.cellSize * j + self.indentation,
                        self.top + self.cellSize * i + self.indentation), (
                                         self.left + self.cellSize * (j + 1) - self.indentation,
                                         self.top + self.cellSize * (i + 1) - self.indentation),
                                     width=2)
                    pygame.draw.line(screen, (0, 0, 255),
                                     (self.left + self.cellSize * (j + 1) - self.indentation,
                                      self.top + self.cellSize * i + self.indentation),
                                     (self.left + self.cellSize * j + self.indentation,
                                      self.top + self.cellSize * (i + 1) - self.indentation),
                                     width=2)

                elif self.board[i][j] == 2:
                    pygame.draw.ellipse(screen, (255, 0, 0), (
                        self.left + self.cellSize * j + self.indentation,
                        self.top + self.cellSize * i + self.indentation, self.cellSize - self.indentation,
                        self.cellSize - self.indentation),
                                        width=2)

    def getCell(self, mousePos):
        if mousePos[0] < self.left or mousePos[1] < self.top or mousePos[0] > self.left + self.cellSize * self.width or \
                mousePos[1] > self.top + self.cellSize * self.height:
            return None
        x = (mousePos[0] - self.left) // self.cellSize
        y = (mousePos[1] - self.top) // self.cellSize
        return (x, y)

    def onClick(self, cellCoords):
        if not cellCoords:
            return
        if self.turn == "cross":
            if self.board[cellCoords[1]][cellCoords[0]] == 0:
                self.board[cellCoords[1]][cellCoords[0]] = 1
                self.turn = "zero"
        if self.turn == "zero":
            if self.board[cellCoords[1]][cellCoords[0]] == 0:
                self.board[cellCoords[1]][cellCoords[0]] = 2
                self.turn = "cross"

    def getClick(self, mousePos):
        cell = self.getCell(mousePos)
        self.onClick(cell)


screen = pygame.display.set_mode((500, 500))
board = Board(4, 3)
board.set_view(10, 10, 100)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.getClick(event.pos)
    screen.fill((0, 0, 0))
    board.render(screen)
    pygame.display.flip()
