from map import draw_map
from classes import *

class Controller():
    def app():
        menu = True
        game = True
        win_lose = False
        while game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    game = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and  menu:
                    x, y = event.pos
                    if btn_start.collidepoint(x,y):
                        menu = False
                        player.rect.x ,player.rect.y = TILE,TILE
                        for tank in tank_grp:
                            tank.xp = 1
                        player.murder = 0
                        win_lose = False
                    if btn_exit.collidepoint(x,y):
                        pygame.quit()
                        game = False
                    
            if game:
                mw.fill(GRAY)
                for block in blocks :
                        block.draw()
                        block.update(tank_grp)

                if not menu :
                    tank_grp.update(blocks,tank_grp)

                    txt_kills.draw()
                    txt_kills.text = "kills : "+str(player.murder)

                    if player.murder == 4 :
                        win_lose = True
                        txt_win_lose.text = t_win
                        menu = True
                        player.murder = 0

                    elif player.xp <= 0 :
                        win_lose = True
                        txt_win_lose.text = t_lose
                        menu = True
                        player.murder = 0

                        
                else:
                    if win_lose :
                        txt_win_lose.draw()

                    enemy_grp.update(blocks,tank_grp)
                    btn_start.update()
                    btn_exit.update()
                    
                pygame.display.flip()
                clock.tick(FPS)

            
blocks = draw_map()

tank_grp = pygame.sprite.Group()
enemy_grp = pygame.sprite.Group()
player = Player("img/green_tank_up.png",-10,-10,TILE,TILE,"green")
enemy_1 = Enemy("img/green_tank_up.png",TILE,8*TILE,TILE,TILE,"green")
enemy_2 = Enemy("img/green_tank_up.png",9*TILE,2*TILE,TILE,TILE,"green")
enemy_3 = Enemy("img/green_tank_up.png",19*TILE,4*TILE,TILE,TILE,"green")
enemy_4 = Enemy("img/green_tank_up.png",22*TILE,10*TILE,TILE,TILE,"green")
tank_grp.add(player)
tank_grp.add(enemy_1)
tank_grp.add(enemy_2)
tank_grp.add(enemy_3)
tank_grp.add(enemy_4)
enemy_grp.add(enemy_1)
enemy_grp.add(enemy_2)
enemy_grp.add(enemy_3)
enemy_grp.add(enemy_4)

btn_start = Picture("img/btn_start.png",WIDTH/2-TILE*4,HEIGHT//2-TILE*3.5,TILE*8,TILE*4)
btn_exit = Picture("img/btn_exit.png",WIDTH/2-TILE*4,HEIGHT//2+TILE*1.5,TILE*8,TILE*4)

txt_kills = TXT(TILE,10,"kills : "+str(player.murder),TILE//1.5)
txt_win_lose = TXT(WIDTH//3,TILE*2,"",TILE)

t_win = "Congratulatins , you win all of them !"
t_lose = "Oh no, you was kiled by a robot, poor guy!"

if __name__ == "__main__":
    Controller.app()