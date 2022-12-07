W_WIDTH = 1200 #whole window size
W_HEIGHT = 900
HEADER_H = 100 #header height, where scores are located during active game
SPEED = 5
CELL_W = 50 # sizes of the cell, images of characters and emeralds should be 50x50 p size
CELL_H = 50
COLS = W_WIDTH/CELL_W #size of the grid
ROWS = W_HEIGHT/CELL_H
PATH = "D:\\NYUAD\\CS\\Final project\\CS-project" # change it to your location in laptop
#D:\\NYUAD\\CS\\Final project\\Digger

DIRS = [RIGHT, UP, LEFT, DOWN] #possible directions of digger
INC = [[1, 0], [0,-1], [-1, 0], [0,1]] # Increments for directions

def keyPressed(): 
    if game.is_game_over: #to read users name when the game is finished
        game.game_over_screen.key_handler(key)    
    elif (key == "P" or key == "p") and game.is_level_active: #doing pause
        game.is_pause = True
    elif key == "Q" or key == "q": #quitting game to welcome screen
        game.quit()
    elif game.is_level_active: #movements of the digger
        game.digger.key_pressed(keyCode)
    elif keyCode == 32: #space bar pressed #pressing space to start the game from welcome screen
        game.welcome_screen.start_game()
        
            
def keyReleased(): #making digger stop when key is released
    if game.is_level_active:
        game.digger.key_released(keyCode)
        

        
def mouseClicked():
    mouse = Coordinates(mouseX, mouseY)
    if game.is_pause: #click during pause to resume the game
        game.pause_screen.click_handler(mouse)
    elif game.is_game_over: #click on gameover screen to go to the welcome screen
        game.game_over_screen.click_handler(mouse)
    elif not game.is_level_active: #click on the welcome screen to start the game
        game.welcome_screen.click_handler(mouse)

class Coordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    

class Level: #configuration of the whole level that is read from files *which we will write ourselves beforehand*
    def __init__(self, level_number):
        self.level_number = level_number
        self.config = open(PATH + "\\levels\\{0}.txt".format(self.level_number))
        """level file:
        color of the ground, number of enemies, probability for enemies to chase you, digger fire recharge time
        number of emeralds (n), n lines with coordinates of emeralds
        number of money bags (m), m lines with coordinates of emeralds
        number of cols and rows in layout of initial maze
        maze itself"""
        self.colour, self.enemies_num, self.enemies_prob, self.recharge_time = self.config.readline().strip().split(", ")
        self.initial_maze = []
        for line in self.config:
            self.initial_maze.append([a for a in line.strip().split(", ")])
        self.config.close()
        self.colour = tuple(map(int, self.colour[1:-1].split(",")))
        self.backgrnd = loadImage(PATH + "\\levels\\{0}.png".format(self.level_number))
        
class Creature:
    def __init__(self, img, row, col):
        self.img = loadImage(PATH + "\\images\\{0}".format(img))
        self.row = row
        self.col = col
    
    def display(self):
        pass
        
        
        
    
class Enemy (Creature): #general enemy class
    def __init__(self):
        pass
        
    def move(self, prob): #logic for enemy
        pass
        
    def display(self):
        pass
    
class Nobbin (Enemy): #goes only on available in maze paths
    def __init__(self):
        pass
    
class Hobbin (Nobbin): #can create paths in maze
    def __init__(self):
        pass
    
class Digger (Creature): #can create paths in maze
    def __init__(self, row, col):
        self.key_handler = None
        self.row = row
        self.col = col
        self.x = row*CELL_H
        self.y = col*CELL_W
        self.dir = DIRS[0]
        self.speed = SPEED
    
    def shoot_fire(self):
        pass
        
        
    def key_pressed(self, pressed_key):
        if keyCode in DIRS:
            game.digger.key_handler = pressed_key 
            self.dir = pressed_key
        
    def key_released(self, released_key):
        if keyCode in DIRS:
            game.digger.key_handler = None
            
    def display(self):
        self.update()
        #animation
        #turning the image according to self.dir
        fill(0)
        rectMode(CORNER)
        rect(self.x, self.y, CELL_W, CELL_H)
        
    def update(self):
        if self.key_handler != None:
            self.x = self.x + self.speed*INC[DIRS.index(self.dir)][0]
            self.y = self.y + self.speed*INC[DIRS.index(self.dir)][1]
            self.update_grid_pos()
            # print(str(self.key_handler))
            
    def update_grid_pos(self):
        self.row = self.y//CELL_H
        self.col = self.x//CELL_W
            
            
    
    
    
class LootItem:
    def __init__(self):
        pass

class Emerald (LootItem):
    def __init__(self):
        pass
    
class MoneyBag (LootItem):
    def __init__(self):
        pass
        
    def gravity(self):
        pass
    
class Cherry (LootItem):
    def __init__(self):
        pass
    
class Maze: #layout of board, where enemies who cannot dig can go, is a graph represented as adjacency list
    def __init__(self, initial_maze):
        self.layout = initial_maze
        
    def update(self, coord): #coord of class Coordinates where digger is now
        #add edges to graph according on digger's position, or Hobbin position
        pass
        
    
class WelcomeScreen:
    def __init__(self):
        pass
        
    def display(self):
        textSize(40)
        rectMode(CENTER)
        text("DIGGER", 0, W_WIDTH//2)
        
    def click_handler(self, coord):
        #game starts upon click
        self.start_game()
        
    def start_game(self): 
        game.is_level_active = True
        background(0)
        
    
class GameOverScreen:
    def __init__(self):
        self.user_name = ""
        
    def key_handler(self, key):
        #recieving user name to write it later in scoreboard
        pass
        
    def display(self):
        pass
        
    def click_handler(self, coord):
        #returns to welcome screen upon click
        game.is_game_over = False
        

class PauseScreen:
    def __init__(self):
        pass
        
    def display(self):
        pass
    
    def click_handler(self):
        #game resumes upon click
        pass

        
class Ground():
    def __init__(self):
        self.layout = []
        self.colour = None
        # initial layout by initial maze
        
    def update(self):
        pass
        
        
class Game:
    def __init__(self):
        self.pause_screen = PauseScreen()
        self.is_level_active = False #only true when person plays the game
        self.level = Level(1) 
        self.maze = Maze(self.level.initial_maze)
        self.is_game_over = False #only true when game over screen is shown. upon click the variable is false and person sees welcome screen
        self.score = 0
        self.enemies = []
        #initialize enemies according to level configuration
        self.emeralds = []
        self.money_bags = []
        #initialize emeralds according to level configuration
        self.welcome_screen = WelcomeScreen()
        self.game_over_screen = GameOverScreen()
        self.pause_screen = PauseScreen()
        self.is_pause = False
        self.digger = Digger(5, 5)
        # self.ground = [] #array of pixels
        # self.init_ground()
        self.ground = Ground()
        
    def display(self):
        if self.is_game_over: 
            self.game_over_screen.display()
        elif not self.is_level_active:
            self.welcome_screen.display()           
        elif self.is_pause:
            self.pause_screen.display()
        else:
            # self.draw_ground()
            image(self.level.backgrnd,0,100)
            self.move_enemies()
            self.digger.display()
            for e in self.enemies:
                e.display()
            for e in self.emeralds:
                e.display()
            for b in self.money_bags:
                b.display()
            self.ground.update()
            
    # def init_ground(self):
    #     for i in range(W_HEIGHT):
    #         temp = []
    #         for j in range(W_WIDTH):
    #             temp.append(0) # 0 - black, 1 - level colour
    #         self.ground.append(temp)
            
    #     for i in range(W_WIDTH):
    #         self.ground[int(sin(i)*10)%W_HEIGHT][i] = 1
    #         # self.ground[i][5] = 1
        
        
    # def draw_ground(self): #sinus function
    #     # print(self.ground)
    #     for i in range(len(self.ground)):
    #         for j in range(len(self.ground[0])):
    #             if self.ground[i][j] == 1:
    #                 stroke(*self.level.colour)
    #             else:
    #                 stroke(0)
    #             # noSmooth()
    #             # fill(3,255,123)
    #             point(i, j)
                
    def move_enemies(self):
        for enemy in self.enemies:
            enemy.move()
            
    def quit(self):
        self.is_game_over = True
        self.is_level_active = False
        
    def add_to_scoreboard(self):
        #writes user to the file
        #file in PATH+"scoreboard.txt"
        pass
    
    

def setup():
    size(W_WIDTH, W_HEIGHT)

game = Game()

def draw():

    game.display()
