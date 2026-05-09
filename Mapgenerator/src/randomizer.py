import pygame
import random
import os

SCREEN_WIDTH=1000
SCREEN_HEIGHT=700
UI_WIDTH=320

DEFAULT_MAP_WIDTH=150
DEFAULT_MAP_HEIGHT=100
DEFAULT_TILE_SIZE=6
DEFAULT_GRID_SIZE=1

IMAGE_FOLDER="imagelibrary"

BLACK=(0,0,0)
WHITE=(255,255,255)

UI_BG=(35,35,35)

BUTTON_COLOR=(70,70,70)
BUTTON_HOVER=(100,100,100)

GRID_COLOR=(20,20,20)

DEEP_WATER=(5,30,120)
SHALLOW_WATER=(30,80,190)
BEACH=(194,178,128)
GRASS=(50,170,70)
FOREST=(25,120,45)
HILLS=(130,120,90)
MOUNTAIN=(150,150,150)
SNOW=(240,240,240)

class Terrain:

    @staticmethod
    def get_color(h):

        if h<40: return DEEP_WATER
        elif h<70: return SHALLOW_WATER
        elif h<85: return BEACH
        elif h<145: return GRASS
        elif h<185: return FOREST
        elif h<220: return HILLS
        elif h<245: return MOUNTAIN
        return SNOW

class Button:

    def __init__(self,x,y,w,h,text,font):
        self.rect=pygame.Rect(x,y,w,h)
        self.text=text
        self.font=font

    def draw(self,screen):
        color=BUTTON_COLOR
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            color=BUTTON_HOVER
        pygame.draw.rect(screen,color,self.rect)
        screen.blit(self.font.render(self.text,True,WHITE),(self.rect.x+10,self.rect.y+10))

    def is_clicked(self,event):
        return event.type==pygame.MOUSEBUTTONDOWN and event.button==1 and self.rect.collidepoint(event.pos)

class InputBox:

    def __init__(self,x,y,w,h,text=""):
        self.rect=pygame.Rect(x,y,w,h)
        self.text=text
        self.active=False
        self.first_click=True

    def handle_event(self,event):

        if event.type==pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active=True
                if self.first_click:
                    self.text=""
                    self.first_click=False
            else:
                self.active=False

        if event.type==pygame.KEYDOWN and self.active:

            if event.key==pygame.K_BACKSPACE:
                self.text=self.text[:-1]

            elif event.key==pygame.K_RETURN:
                self.active=False

            else:
                # NOW supports decimals
                if event.unicode.isdigit() or event.unicode==".":
                    if event.unicode=="." and "." in self.text:
                        return
                    self.text+=event.unicode

    def draw(self,screen,font):
        color=(110,110,110) if self.active else (70,70,70)
        border=(255,255,255) if self.active else (40,40,40)

        pygame.draw.rect(screen,color,self.rect)
        pygame.draw.rect(screen,border,self.rect,2)

        screen.blit(font.render(self.text,True,WHITE),(self.rect.x+5,self.rect.y+7))

    def get_value(self,fallback):
        try:
            v=float(self.text)   # IMPORTANT CHANGE
            return v if v>0 else fallback
        except:
            return fallback

class MapGenerator:

    def __init__(self,w,h):
        self.w=w
        self.h=h
        self.map=[]

    def apply_noise(self):
        for y in range(self.h):
            for x in range(self.w):
                self.map[y][x]+=random.randint(-25,25)

    def smooth(self,p):

        for _ in range(p):
            new=[]
            for y in range(self.h):
                row=[]
                for x in range(self.w):

                    s=0
                    c=0

                    for dy in (-1,0,1):
                        for dx in (-1,0,1):

                            nx=x+dx
                            ny=y+dy

                            if 0<=nx<self.w and 0<=ny<self.h:
                                s+=self.map[ny][nx]
                                c+=1

                    row.append(s//c)

                new.append(row)

            self.map=new

    def generate_random(self):

        self.map=[[random.randint(0,120) for _ in range(self.w)] for _ in range(self.h)]

        self.smooth(3)

        for _ in range(random.randint(4,7)):

            cx=random.randint(0,self.w-1)
            cy=random.randint(0,self.h-1)
            r=random.randint(min(self.w,self.h)//8,min(self.w,self.h)//4)

            for y in range(self.h):
                for x in range(self.w):

                    dx=x-cx
                    dy=y-cy
                    d=(dx*dx+dy*dy)**0.5

                    if d<r:
                        self.map[y][x]+=int((1-d/r)*180)

        for _ in range(random.randint(3,6)):

            ox=random.randint(0,self.w)
            oy=random.randint(0,self.h)
            r=random.randint(min(self.w,self.h)//6,min(self.w,self.h)//3)

            for y in range(self.h):
                for x in range(self.w):

                    dx=x-ox
                    dy=y-oy
                    d=(dx*dx+dy*dy)**0.5

                    if d<r:
                        self.map[y][x]-=int((1-d/r)*200)

        for _ in range(random.randint(4,8)):

            x=random.randint(0,self.w-1)
            y=random.randint(0,self.h-1)

            for _ in range(random.randint(40,120)):

                if 0<=x<self.w and 0<=y<self.h:

                    self.map[y][x]+=random.randint(60,120)

                    for oy in (-1,0,1):
                        for ox in (-1,0,1):

                            nx=x+ox
                            ny=y+oy

                            if 0<=nx<self.w and 0<=ny<self.h:
                                self.map[ny][nx]+=random.randint(10,40)

                x+=random.randint(-1,1)
                y+=random.randint(-1,1)

        self.apply_noise()
        self.smooth(2)

        for y in range(self.h):
            for x in range(self.w):
                self.map[y][x]=max(0,min(255,self.map[y][x]))

    def from_heightmap(self,path):

        img=pygame.image.load(path)
        img=img.convert_alpha() if img.get_alpha() else img.convert()
        img=pygame.transform.scale(img,(self.w,self.h))

        self.map=[]

        for y in range(self.h):
            self.map.append([
                sum(img.get_at((x,y))[:3])//3
                for x in range(self.w)
            ])

        self.smooth(2)

    def draw(self,screen,tile,grid):

        grid=int(max(0.2,round(grid)))  # DECIMAL SAFE GRID FIX

        for y in range(self.h):
            for x in range(self.w):

                r=pygame.Rect(
                    UI_WIDTH+x*tile,
                    y*tile,
                    tile,
                    tile
                )

                pygame.draw.rect(screen,Terrain.get_color(self.map[y][x]),r)

                if grid>0 and tile>1:
                    pygame.draw.rect(screen,GRID_COLOR,r,grid)

def get_maps():

    base_dir=os.path.dirname(os.path.abspath(__file__))
    folder=os.path.join(base_dir,IMAGE_FOLDER)

    if not os.path.exists(folder):
        os.makedirs(folder)

    return [
        os.path.join(folder,f)
        for f in os.listdir(folder)
        if f.lower().endswith((".png",".jpg",".jpeg",".bmp"))
    ]

def main():

    pygame.init()

    screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    clock=pygame.time.Clock()

    font=pygame.font.SysFont("arial",22)
    small=pygame.font.SysFont("arial",16)

    w_in=InputBox(20,70,100,40,str(DEFAULT_MAP_WIDTH))
    h_in=InputBox(140,70,100,40,str(DEFAULT_MAP_HEIGHT))
    t_in=InputBox(20,150,100,40,str(DEFAULT_TILE_SIZE))
    g_in=InputBox(140,150,100,40,str(DEFAULT_GRID_SIZE))

    rand=Button(20,250,280,50,"Generate Random",font)
    hm=Button(20,320,280,50,"Generate Heightmap",font)

    gen=MapGenerator(DEFAULT_MAP_WIDTH,DEFAULT_MAP_HEIGHT)
    gen.generate_random()

    tile=DEFAULT_TILE_SIZE
    grid=DEFAULT_GRID_SIZE

    run=True

    while run:

        screen.fill(BLACK)

        for e in pygame.event.get():

            if e.type==pygame.QUIT:
                run=False

            if e.type==pygame.KEYDOWN and e.key==pygame.K_ESCAPE:
                run=False

            w_in.handle_event(e)
            h_in.handle_event(e)
            t_in.handle_event(e)
            g_in.handle_event(e)

            if rand.is_clicked(e):

                gen=MapGenerator(
                    int(w_in.get_value(DEFAULT_MAP_WIDTH)),
                    int(h_in.get_value(DEFAULT_MAP_HEIGHT))
                )

                tile=max(2,int(t_in.get_value(DEFAULT_TILE_SIZE)))
                grid=g_in.get_value(DEFAULT_GRID_SIZE)

                gen.generate_random()

            if hm.is_clicked(e):

                files=get_maps()

                if files:

                    gen=MapGenerator(
                        int(w_in.get_value(DEFAULT_MAP_WIDTH)),
                        int(h_in.get_value(DEFAULT_MAP_HEIGHT))
                    )

                    tile=max(2,int(t_in.get_value(DEFAULT_TILE_SIZE)))
                    grid=g_in.get_value(DEFAULT_GRID_SIZE)

                    gen.from_heightmap(random.choice(files))

        gen.draw(screen,tile,grid)

        pygame.draw.rect(screen,UI_BG,(0,0,UI_WIDTH,SCREEN_HEIGHT))

        screen.blit(font.render("MAP GENERATOR",True,WHITE),(20,20))

        screen.blit(small.render("Width",True,WHITE),(20,50))
        screen.blit(small.render("Height",True,WHITE),(160,50))
        screen.blit(small.render("Tile",True,WHITE),(20,120))
        screen.blit(small.render("Grid",True,WHITE),(160,120))

        w_in.draw(screen,font)
        h_in.draw(screen,font)
        t_in.draw(screen,font)
        g_in.draw(screen,font)

        rand.draw(screen)
        hm.draw(screen)

        info=[
            "WARNING:",
            "Tile size under 2 will break rendering.",
            "",
            "Any grid value at or below 5 will remove grids.",
            "Width/Height = Map size.",
            "Tile = Zoom level.",
            "Grid = Border thickness of pixels.",
            "",
            "Supports custom heightmaps (imagelibrary folder)"
        ]

        y=420

        for i in info:
            screen.blit(small.render(i,True,WHITE),(20,y))
            y+=18

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__=="__main__":
    main()