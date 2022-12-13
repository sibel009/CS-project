from collections import deque 
from random import randint

DISPLAY_GRID = False #False
W_WIDTH = 1200 #whole window size
W_HEIGHT = 900
HEADER_H = 100 #header height, where scores are located during active game
SPEED = 5
CELL_W = 80 # sizes of the cell, images of characters and emeralds should be 50x50 p size
CELL_H = 80
COLS = W_WIDTH/CELL_W #size of the grid
ROWS = (W_HEIGHT-HEADER_H)/CELL_H
PATH = "D:\\NYUAD\\CS\\Final project\\CS-project" # change it to your location in laptop
#D:\\NYUAD\\CS\\Final project\\Digger

DIRS = [RIGHT, UP, LEFT, DOWN] #possible directions of digger
INC = [[1, 0], [0,-1], [-1, 0], [0,1]] # Increments for directions

def keyPressed(): 
    if game.is_game_over: #to read users name when the game is finished
        game.game_over_screen.key_handler(keyCode)    
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
    mouse = Point(mouseX, mouseY)
    if game.is_pause: #click during pause to resume the game
        game.pause_screen.click_handler(mouse)
    elif game.is_game_over: #click on gameover screen to go to the welcome screen
        game.game_over_screen.click_handler(mouse)
    elif not game.is_level_active: #click on the welcome screen to start the game
        game.welcome_screen.click_handler(mouse)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        if self.x == other.x and self.y == other.y:
            return True
        else: 
            return False
        
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __str__(self):
        return str(self.x)+", "+str(self.y)

class Level: #configuration of the whole level that is read from files *which we will write ourselves beforehand*
    def __init__(self, level_number):
        self.level_number = level_number
        self.config = open(PATH + "\\levels\\{0}.txt".format(self.level_number))
        """level file:
        color of the ground, number of enemies, enemies speed, probability for enemies to chase you, digger fire recharge time
        number of emeralds (n), 
        n lines with coordinates of emeralds
        number of money bags (m), 
        m lines with coordinates of bags
        number of cols and rows in layout of initial maze
        maze itself"""
        vars = self.config.readline().strip().split(", ")
        self.colour = vars[0]
        self.enemies_num, self.enemies_speed, self.enemies_prob, self.recharge_time = map(int, vars[1:])
        self.emeralds_num = int(self.config.readline())
        self.emeralds_pos = []
        for i in range(self.emeralds_num):
            x, y = self.config.readline().strip().split(", ")
            self.emeralds_pos.append(Point(x, y))
            
        self.money_bags_num = int(self.config.readline())
        self.money_bags_pos = []
        for i in range(self.money_bags_num):
            x, y = self.config.readline().strip().split(", ")
            self.money_bags_pos.append(Point(x, y))
            
        self.maze_rows, self.maze_cols = map(int, self.config.readline().strip().split(", "))
        self.maze = []
        for i in range(self.maze_rows):
            temp = map(int, self.config.readline().strip().split(", "))
            self.maze.append(temp)

        self.config.close()
        self.colour = tuple(map(int, self.colour[1:-1].split(",")))
        self.backgrnd = loadImage(PATH + "\\levels\\{0}.png".format(self.level_number))
        
class Creature:
    def __init__(self, img, row, col, colour, speed = SPEED):
        # self.img = loadImage(PATH + "\\images\\{0}".format(img))
        self.row = row
        self.col = col
        self.x = col*CELL_W
        self.y = row*CELL_H+HEADER_H
        self.dir = DIRS[2]
        self.speed = speed
        self.tunnel_gap = 15
        self.colour = colour
   
    
      
    # def display(self):
    #     # print(self.key_handler, keyCode)
        
    #     print("COORD1", self.x, self.y)
    #     self.erase()
    #     self.update()
    #     #animation
    #     #turning the image according to self.dir
    #     fill(*self.colour)        
    #     rectMode(CORNER)
    #     rect(self.x+self.tunnel_gap, self.y+self.tunnel_gap, CELL_W-self.tunnel_gap*2, CELL_H-self.tunnel_gap*2)
    #     print("COORD2", self.x, self.y)
        
        
    
# class Enemy (Creature): #general enemy class
#     def __init__(self):
#         pass

    
class Nobbin (Creature): #goes only on available in maze paths
    def __init__(self, row, col, speed, delay = 0, update_gap = 50):
        Creature.__init__(self, "nobbin.png", row, col, (255,0,0), speed)
        self.path = []
        self.initial_frame = -1
        self.last_updated = -1 #frame when path was last updated
        self.delay = delay
        self.update_gap = update_gap
        self.ignore_prob = 10
        # self.is_rand = False
        
    def erase(self):
        fill(*game.ground.colour)
        rectMode(CORNER)
        rect(self.x+self.tunnel_gap-self.speed*INC[DIRS.index(self.dir)][0], self.y+self.tunnel_gap-self.speed*INC[DIRS.index(self.dir)][1], CELL_W-self.tunnel_gap*2, CELL_H-self.tunnel_gap*2)
        
      
    def display(self):
        if self.initial_frame == -1:
            self.initial_frame = frameCount
            self.last_updated = frameCount
        # print(self.key_handler, keyCode)
        if frameCount - self.initial_frame > self.delay:
        # print("COORD1", self.x, self.y)
        #animation
        #turning the image according to self.dir
            self.erase()
            fill(*self.colour)        
            rectMode(CORNER)
            rect(self.x+self.tunnel_gap, self.y+self.tunnel_gap, CELL_W-self.tunnel_gap*2, CELL_H-self.tunnel_gap*2)
            # print("DRAWN AT", self.x, self.y)
            # print("COORD2", self.x, self.y)
            self.update()
        
    def update(self): #logic for enemy
        # print("FRAMECOUNT", frameCount)
        # if frameCount == 75:
        #     self.bfs()
        #     self.update_dir()
        # print(self.dir)
        if len(self.path) <= 3 or frameCount - self.last_updated > self.update_gap:
            self.last_updated = frameCount
            self.bfs()
        if self.x % CELL_W == 0 and (self.y-HEADER_H) % CELL_H == 0:
            self.update_dir()
        self.check_collision()
            
            #checking if he is allowed to go in direction of self.dir
        if (self.x % CELL_W != 0 or (self.y-HEADER_H) % CELL_H != 0) or game.maze.adj[self.row][self.col][DIRS.index(self.dir)] == 1:
            self.x = min(max(0, self.x + self.speed*INC[DIRS.index(self.dir)][0]), W_WIDTH-CELL_W)
            self.y = min(max(HEADER_H, self.y + self.speed*INC[DIRS.index(self.dir)][1]), W_HEIGHT-CELL_H)

        self.update_grid_pos()
            
            # print("MY POSITION", self.x, self.y, self.row, self.col, INC[DIRS.index(self.dir)])
        
        
    def update_grid_pos(self):
        # prev = Point(self.row, self.col)
        self.row = (self.y-HEADER_H)//CELL_H 
        self.col = (self.x)//CELL_W
        # new = Point(self.row, self.col)
        # if prev != new and len(self.path) > 2:
        #     print("new grid pos", prev.x, prev.y, new.x, new.y)
            # self.update_dir()
    
    def update_any_dir(self):
        adj = game.maze.adj[self.row][self.col]
        for i in range(4):
            if adj[i] == 1:
                self.dir = DIRS[i]
        
    def update_dir(self):
        # print "PATH"
        # for p in self.path:
            # print(p)
        # print("popped", popped.x, popped.y, len(self.path))
        if randint(0,100) < self.ignore_prob and max(game.maze.adj[self.row][self.col][(DIRS.index(self.dir)+1)%4], game.maze.adj[self.row][self.col][(DIRS.index(self.dir)+3)%4]):
            prev_dir = self.dir
            self.dir = DIRS[randint(0,3)]
            while game.maze.adj[self.row][self.col][DIRS.index(self.dir)] == 0 or abs(DIRS.index(prev_dir) - DIRS.index(self.dir)) == 2:
                self.dir = DIRS[randint(0,3)] 
            self.path = []            
        else:
            while len(self.path) > 0 and self.path[0] != Point(self.row, self.col):
                self.path.pop(0)
            if len(self.path) >= 2:
                # print("upd dir", [self.path[1].y - self.path[0].y, self.path[1].x - self.path[0].x])
                self.dir = DIRS[INC.index([self.path[1].y - self.path[0].y, self.path[1].x - self.path[0].x])]
                popped = self.path.pop(0)
            
       
    def check_collision(self):
        if self.row == game.digger.row and self.col == game.digger.col:
            game.end_game()
        elif abs(self.x - game.digger.x) < CELL_W and self.row == game.digger.row and game.maze.adj[self.row][self.col][DIRS.index(self.dir)] == 1:
            game.end_game()
        elif abs(self.y - game.digger.y) < CELL_H and self.col == game.digger.col and game.maze.adj[self.row][self.col][DIRS.index(self.dir)] == 1:
            game.end_game()
        
                
    def bfs(self):
        # print("KLYKALY")
        plan = deque()
        start = Point(self.row, self.col)
        plan.append(start)
        visited = [[-1 for j in range(COLS)] for i in range(ROWS)]
        visited[self.row][self.col] = start
        last = Point(-1,-1)
        while len(plan) > 0:
            v = plan.popleft()
            # print("now visiting", v.x, v.y)
            if v.x == game.digger.row and v.y == game.digger.col:
                last = v
                break
            adj = game.maze.adj[v.x][v.y]
            for i in range(4):
                u = Point(v.x+INC[i][1], v.y + INC[i][0])
                if u.x >= 0 and u.x < ROWS and u.y >= 0 and u.y < COLS:
                    if adj[i] == 1 and visited[u.x][u.y] == -1:
                        visited[u.x][u.y] = v
                        plan.append(u)
                    
        #backtracking path
        if last == Point(-1,-1):
            # print(game.maze.adj)
            pass
        else:
            self.path = []
            while last != start:
                self.path.append(last)
                # print("last", last.x, last.y)
                last = visited[last.x][last.y]
            self.path.append(start)
            self.path.reverse()
        # print "PATH"
        # for p in self.path:
        #     print(p)
            
    
class Hobbin (Nobbin): #can create paths in maze
    def __init__(self):
        pass
        
    def update(self, prob): #logic for enemy
        pass
    
class Digger (Creature): #can create paths in maze
    def __init__(self, row, col):
        self.key_handler = None
        Creature.__init__(self, "digger.png", row, col, (0,0,0))
        # self.img_size = CELL_W - self.tunnel_gap
    
    def shoot_fire(self):
        pass
        
 
      
    def display(self):
        # print(self.key_handler, keyCode)
        
        # print("COORD1", self.x, self.y)
        self.erase()
        self.update()
        #animation
        #turning the image according to self.dir
        fill(*self.colour)        
        rectMode(CORNER)
        rect(self.x+self.tunnel_gap, self.y+self.tunnel_gap, CELL_W-self.tunnel_gap*2, CELL_H-self.tunnel_gap*2)
        # print("COORD2", self.x, self.y)
        
              
    def erase(self):
        fill(*game.ground.colour)
        rectMode(CORNER)
        rect(self.x+self.tunnel_gap, self.y+self.tunnel_gap, CELL_W-self.tunnel_gap*2, CELL_H-self.tunnel_gap*2)
    
    def key_pressed(self, pressed_key):
        # if pressed_key not in self.key_handler:
        #     self.key_handler.append(pressed_key)
        if self.key_handler != pressed_key and pressed_key in DIRS:
            self.key_handler = pressed_key 
            # self.dir = pressed_key
        
    def key_released(self, released_key):
        # try:
        #     self.key_handler.remove(released_key)
        # except:
            # pass
        if released_key in DIRS and self.key_handler == released_key:
            self.key_handler = None
     
    
    
    def update(self):
        # print(self.key_handler)
        if self.key_handler != None:
            # self.update_grid_pos()
            # print(str(self.key_handler))
            if self.dir != self.key_handler and abs(DIRS.index(self.dir)-DIRS.index(self.key_handler)) == 2: 
                self.dir = self.key_handler
                # print("dd")
            elif  self.dir != self.key_handler and self.x % CELL_W == 0 and (self.y-HEADER_H) % CELL_H == 0:
                self.dir = self.key_handler
                game.ground.add_circle()
            self.x = min(max(0, self.x + self.speed*INC[DIRS.index(self.dir)][0]), W_WIDTH-CELL_W)
            self.y = min(max(HEADER_H, self.y + self.speed*INC[DIRS.index(self.dir)][1]), W_HEIGHT-CELL_H)
        self.update_grid_pos()
  
    # def is_movement_possible(self, dir):
    #     print(self.col, self.row)
    #     if self.col + INC[DIRS.index(dir)][0] < 0 or self.col + INC[DIRS.index(dir)][0] >= COLS:
    #         return False
    #     elif self.row + INC[DIRS.index(dir)][1] < 0 or self.row + INC[DIRS.index(dir)][1]  >= ROWS:
    #         return False
    #     else:
    #         return True
        
            
    def update_grid_pos(self):
        prev = Point(self.col, self.row)
        self.row = (self.y-HEADER_H)//CELL_H
        self.col = self.x//CELL_W
        new = Point(self.col, self.row)
        if prev != new:
            game.maze.update(prev, new)       
            
    
    
    
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
        self.layout = initial_maze[:]
        self.adj = [] #adjacency list
        for i in range(ROWS):
            temp = []
            for j in range(COLS):
                temp2 = []
                #0,1
                if i == 0 and j == 10:
                    for a in self.layout:
                        print(a)
                for inc_x, inc_y in INC:
                    if self.layout[i][j] == 1 and i+inc_y >= 0 and i+inc_y < ROWS and j+inc_x >= 0 and j+inc_x < COLS and self.layout[i+inc_y][j+inc_x] == 1:
                        temp2.append(1)
                    else:
                        temp2.append(0)
                temp.append(temp2)
            self.adj.append(temp)
        print(self.adj)
        # for i in range(ROWS):
        #     for j in range(COLS):
        #         if sum(self.adj[i][j]) > 0:
        #             print(i, j, sum(self.adj[i][j]))
        
        
    def update(self, prev, new): #coord of class Point where digger is now, and where it came from (col and row)
        #add edges to graph according on digger's position, or Hobbin position
        # print([new.x - prev.x, new.y - prev.y])
        idx = INC.index([new.x - prev.x, new.y - prev.y])
        self.adj[prev.y][prev.x][idx] = 1
        self.adj[new.y][new.x][(idx+2)%4] = 1 # creating edge in other direction
        
        
    
class WelcomeScreen:
    def __init__(self):
        pass
        
    def display(self):
        background(123)
        textSize(40)
        rectMode(CENTER)
        text("DIGGER", 0, W_WIDTH//2)
        
    def click_handler(self, coord):
        #game starts upon click
        self.start_game()
        
    def start_game(self): 
        game.is_level_active = True
        background(0)
        game.game_setup()
        
    
class GameOverScreen:
    def __init__(self):
        self.user_name = ""
        
    def key_handler(self, key_pressed):
        #recieving user name to write it later in scoreboard
        if key_pressed == 32:
            game.is_game_over = False
        
    def display(self):
        background(0)
        rectMode(CENTER)
        text("GAME OVER", W_WIDTH//2, W_HEIGHT//2)
        
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
    def __init__(self, layout):
        self.layout = []
        self.colour = (139,69,19)
        self.initial_layout = layout
        self.gap = 30
        self.wall_w = 5
        # initial layout by initial maze
        
    def display_initial_layout(self):
        for i in range(ROWS):
            for j in range(COLS):
                # print(ROWS, COLS)
                if self.initial_layout[i][j] == 1:
                    fill(*self.colour)
                    ellipseMode(CORNER)
                    noStroke()
                    circle(j*CELL_W+self.wall_w, i*CELL_H+HEADER_H+self.wall_w, CELL_W-self.wall_w)
                    for inc_x, inc_y in INC:
                        # print(i, j, inc_x, inc_y)
                        if i+inc_y >= 0 and i+inc_y < ROWS and j+inc_x >= 0 and j+inc_x < COLS and self.initial_layout[i+inc_y][j+inc_x] == 1:
                            circle(j*CELL_W+inc_x*self.gap+self.wall_w, i*CELL_H+HEADER_H+inc_y*self.gap+self.wall_w, CELL_W-self.wall_w)
                    # rect(10,10,10,10)
                    # circle(10,10,10)
                # print(2)
    
        
    def update(self):
        if self.layout == []:
            self.layout.append(Point(game.digger.x, game.digger.y))
        elif abs(self.layout[-1].x - game.digger.x) > self.gap or abs(self.layout[-1].y - game.digger.y) > self.gap:
            self.layout.append(Point(game.digger.x, game.digger.y))
            
    def add_circle(self):
        self.layout.append(Point(game.digger.x, game.digger.y))
    
    def display(self):
        # for c in self.layout:
        #     fill(*self.colour)
        #     noStroke()
        #     ellipseMode(CORNER)
        #     circle(c.x, c.y, CELL_W-2)
        
        self.update()
        if self.layout:
            c = self.layout[-1]
            fill(*self.colour)
            noStroke()
            ellipseMode(CORNER)
            circle(c.x+self.wall_w, c.y+self.wall_w, CELL_W-self.wall_w)
    
        
        
        
        
class Game:
    def __init__(self):
        self.pause_screen = PauseScreen()
        self.is_level_active = False #only true when person plays the game
        self.level = Level(1) 
        self.maze = Maze(self.level.maze)
        self.is_game_over = False #only true when game over screen is shown. upon click the variable is false and person sees welcome screen
        self.score = 0
        self.enemies = []
        #initialize enemies according to level configuration
        for i in range(self.level.enemies_num):
            self.enemies.append(Nobbin(0, COLS-1, self.level.enemies_speed))  
        self.enemies.append(Nobbin(0, COLS-1, self.level.enemies_speed-1, 200, 200))  
        self.enemies.append(Nobbin(0, COLS-1, self.level.enemies_speed, 400, 10))         
        self.emeralds = []
        self.money_bags = []
        #initialize emeralds according to level configuration
        self.welcome_screen = WelcomeScreen()
        self.game_over_screen = GameOverScreen()
        self.pause_screen = PauseScreen()
        self.is_pause = False
        self.digger = Digger(ROWS-1, COLS//2)
        # self.ground = [] #array of pixels
        # self.init_ground()
        self.ground = Ground(self.maze.layout)
        
    def game_setup(self):
        self.__init__()
        self.is_level_active = True
        image(self.level.backgrnd,0,HEADER_H)
        self.ground.display_initial_layout()
        # for e in self.enemies:
        #     e.bfs()
        
    def display(self):
        if self.is_game_over: 
            self.game_over_screen.display()
        elif not self.is_level_active:
            self.welcome_screen.display()           
        elif self.is_pause:
            self.pause_screen.display()
        else:
            # self.draw_ground()
            # image(self.level.backgrnd,0,100)
            # self.update_enemies()
            self.ground.display()
            self.digger.display()
            for e in self.enemies:
                e.display()
            for e in self.emeralds:
                e.display()
            for b in self.money_bags:
                b.display()
            if DISPLAY_GRID:
                self.display_grid()
            
    def display_grid(self):
        for i in range(COLS):
            stroke(0)
            line(i*CELL_W, 0, i*CELL_W, W_HEIGHT)
        
        for i in range(ROWS):
            stroke(0)
            line(0, i*CELL_H+HEADER_H, W_WIDTH, i*CELL_H+HEADER_H)
            
            
    def end_game(self):
        self.is_game_over = True
        self.is_level_active = False
        
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
                
    # def update_enemies(self):
    #     for enemy in self.enemies:
    #         enemy.update()
            
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
    # print("yes yes yes")
    game.display()
