import math
import classes
import data
import pygame


def initialize():
    pygame.init()
    pygame.font.init()
    data.despawners.append(classes.Despawner())
    data.spawners.append(classes.Spawner())
    data.obstacles.append(classes.Obstacle(0, 320, 1366, 450))


def cheatcode(key):
    data.cheat_code += key
    if len(data.cheat_code) > 20:
        data.cheat_code = ""
    if "gold" in data.cheat_code:
        data.cheat_code = ""
        data.gold += 999999999


def events():
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
        if e.type == pygame.KEYDOWN:

            print(int(e.key) - 48)
            data.bloons.append(classes.Bloon(int(e.key) - 48))

            try:
                cheatcode(chr(e.key))
            except:
                pass

        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == pygame.BUTTON_LEFT:
                on_click()
            if e.button == pygame.BUTTON_RIGHT:
                on_right_click()


def tick_objects():
    data.screen.blit(data.bg, (0, 0))

    for x in data.bloons:
        x.tick()

    for x in data.towers:
        x.tick()

    for x in data.projectiles:
        x.tick()

    for x in data.spawners:
        x.tick()

    for x in data.despawners:
        x.tick()

    for x in data.traps:
        x.tick()


def draw():

    draw_text(data.health, 47,5)
    draw_text(data.gold, 187, 5)
    if data.show_tower_menu:
        data.screen.blit(data.tower_menu, (0, 50))
        pygame.draw.circle(data.screen, (255, 0, 0), (data.selectedTower.offset[0], data.selectedTower.offset[1]), data.selectedTower.currentRange, 1)
        draw_text(data.selectedTower.pops, 109,76)
        if data.selectedTower.buffed:
            data.screen.blit(data.buff_icon, (data.selectedTower.offset[0], data.selectedTower.y - 20))
        data.screen.blit(data.towers_png[data.selectedTower.id], (68, 120))
        draw_text(data.tower_names[data.selectedTower.id], 40,250)

        sell_price = int(data.tower_stats[data.selectedTower.id][0] / 2)
        if data.selectedTower.id == 7:
            sell_price = 2
        draw_text(sell_price,58,600)

        draw_text(data.tower_upgrade_names[data.selectedTower.id][0][data.selectedTower.upgrade1 - 1], 40, 320, 20)
        draw_text(data.tower_upgrade_names[data.selectedTower.id][1][data.selectedTower.upgrade2 - 1], 40, 420, 20)
        draw_text(data.tower_upgrade_names[data.selectedTower.id][2][data.selectedTower.upgrade3 - 1], 40, 520, 20)

        mouse_x = pygame.mouse.get_pos()[0]
        mouse_y = pygame.mouse.get_pos()[1]

        for i in range(0,3):
            if mouse_x > 140 and mouse_x < 250 and mouse_y > 300 + 90*i and mouse_y < 390 + 90*i:
                draw_text(data.tower_upgrade_descriptions[data.selectedTower.id][i], mouse_x + 100, mouse_y)
                break

        if data.selectedTower.upgrade1 == 5:
            draw_text("MAX LEVEL", 143, 283, 28)
        else:
            draw_text(data.tower_upgrade_names[data.selectedTower.id][0][data.selectedTower.upgrade1], 143, 283, 28)
            draw_text(str(data.tower_upgrade_costs[data.selectedTower.id][0][data.selectedTower.upgrade1])+"$", 143, 340, 28)

        if data.selectedTower.upgrade2 == 5:
            draw_text("MAX LEVEL", 143, 380, 28)
        else:
            draw_text(data.tower_upgrade_names[data.selectedTower.id][1][data.selectedTower.upgrade2], 143, 380, 28)
            draw_text(str(data.tower_upgrade_costs[data.selectedTower.id][1][data.selectedTower.upgrade2])+"$", 143, 420, 28)

        if data.selectedTower.upgrade3 == 5:
            draw_text("MAX LEVEL", 143, 496, 28)
        else:
            draw_text(data.tower_upgrade_names[data.selectedTower.id][2][data.selectedTower.upgrade3], 143, 496, 28)
            draw_text(str(data.tower_upgrade_costs[data.selectedTower.id][2][data.selectedTower.upgrade3])+"$", 143, 540, 28)

        for i in range(0,data.selectedTower.upgrade1):
            pygame.draw.rect(data.screen, (0,255,0), (16, 301+15*i, 13, 14))

        for i in range(0,data.selectedTower.upgrade2):
            pygame.draw.rect(data.screen, (0,255,0), (16, 400+15*i, 13, 14))

        for i in range(0,data.selectedTower.upgrade3):
            pygame.draw.rect(data.screen, (0,255,0), (16, 500+15*i, 13, 14))

    if data.placing_tower:
        data.screen.blit(data.towers_png[data.select], (pygame.mouse.get_pos()[0] - int(data.towers_png[data.select].get_size()[0]/2),pygame.mouse.get_pos()[1] - int(data.towers_png[data.select].get_size()[1]/2)))
        draw_text("RIGHT CLICK TO CANCEL",200,600)
    data.screen.blit(data.menu, (1171,0))
    data.screen.blit(data.health_gold, (0,0))
    draw_text("Round "+str(data.round),0,45)

    if data.health <= 0:
        draw_text("GAME OVER",500,350)


def update():
    data.clock.tick(data.fps)
    pygame.display.flip()



def distance(x1, x2, y1, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def get_angle(tx, ty, bx, by):
    return math.atan2(by - ty, bx - tx)


def add_trap(x, y, lifespan, hp, damage, owner):
    data.traps.append(classes.Trap(x, y, lifespan, hp, damage, owner))


def is_bloon_in_range(tower, bloon=None):

    if bloon is not None:
        if distance(bloon.x + bloon.offset[0], tower.offset[0], bloon.y + bloon.offset[1], tower.offset[1]) < tower.currentRange:
            return True

    for i in data.bloons:
        if distance(i.x + i.offset[0], tower.offset[0], i.y + i.offset[1], tower.offset[1]) < tower.currentRange:
            return i
    return False


def damage_bloon(bloon, attack):

    print("LEVEL", bloon.level)
    print("HP", bloon.hp)

    while attack.damage > 0 and bloon.hp > 0:
        attack.owner.pops += 1
        bloon.hp -= 1
        attack.damage -= 1
        data.gold += 1

    if bloon.hp <= 0:

        if bloon.level <= 0:
            if bloon in data.bloons:
                data.bloons.remove(bloon)
                del bloon
                return


        bloon_list = []
        for i in range(0, data.bloon_children[bloon.level][1]):
            print("XD")
            bloon_list.append(classes.Bloon(data.bloon_children[bloon.level][0],bloon.x - i * 10, bloon.y))
            data.bloons.append(classes.Bloon(data.bloon_children[bloon.level][0], bloon.x - i*10, bloon.y))


        if bloon in data.bloons:
            data.bloons.remove(bloon)
            del bloon


        # for i in bloon_list:
        #     data.bloons.append()

        # data.bloons.remove(bloon)
        # del bloon

    # bloon_list = []
    # for i in range(data.bloonCount-1,-1,-1):
    #     bloon_list.append(int(bloon.hp / 2**i))
    #     bloon.hp -= int(bloon.hp / 2**i) * 2**i

    # position = bloon.x
    # level = 0
    # for i in range(len(bloon_list)-1,-1,-1):
    #     for j in range(0,bloon_list[i]):
    #         data.bloons.append(classes.Bloon(level, position))
    #         if attack.owner.id == 4:
    #             data.bloons[len(data.bloons)-1].gusd = True
    #         position -= 10
    #     level += 1


    return


def draw_text(text, x, y, size=50, color=(255,255,255)):
    font = pygame.font.SysFont("Arial", size - 3)
    test = font.render(str(text), True, color)
    data.screen.blit(test, (x, y))


def sell_tower(tower):
    if tower.id == 7:
        data.gold += 2
    else:
        data.gold += int(data.tower_stats[tower.id][0] / 2)
    data.towers.remove(tower)
    del tower
    data.show_tower_menu = False


def on_click():

    mouse_x = pygame.mouse.get_pos()[0]
    mouse_y = pygame.mouse.get_pos()[1]

    # Place tower

    if data.round == 0:
        if mouse_x > 1267 and mouse_x < 1340 and mouse_y > 686 and mouse_y < 758:
            data.round = 1

    if data.placing_tower and data.gold >= data.tower_stats[data.select][0]:

        if data.select == 4:
            for i in data.towers:
                if i.id == 4:
                    return

        x_off = int(data.towers_png[data.select].get_size()[0]/2)
        y_off = int(data.towers_png[data.select].get_size()[1]/2)
        for i in data.obstacles:
            if mouse_x + x_off > i.x1 and mouse_x - x_off < i.x2 and mouse_y + y_off > i.y1 and mouse_y - y_off < i.y2:
                return

        for i in data.towers:
            if mouse_x + x_off > i.x and mouse_x - x_off < i.x + data.towers_png[i.id].get_size()[0] and mouse_y + y_off > i.y and mouse_y - y_off < i.y + data.towers_png[i.id].get_size()[1]:
                return

        data.placing_tower = False
        data.towers.append(classes.Tower(data.select))
        data.gold -= data.tower_stats[data.select][0]
        return

    if data.show_tower_menu and mouse_x > 240 and mouse_x < 270 and mouse_y > 50 and mouse_y < 80:
        data.show_tower_menu = False

    if data.show_tower_menu and mouse_x>0 and mouse_x < 270 and mouse_y > 50 and mouse_y < 650:
        if mouse_x > 150 and mouse_x < 250 and mouse_y > 600 and mouse_y < 650:
            sell_tower(data.selectedTower)

        for i in range(0,3):
            if mouse_x > 140 and mouse_x < 250 and mouse_y > 300 + 90*i and mouse_y < 390 + 90*i:
                if i==0 and data.selectedTower.upgrade1 < 5 and data.gold >= data.tower_upgrade_costs[data.selectedTower.id][0][data.selectedTower.upgrade1]:
                    data.gold -= data.tower_upgrade_costs[data.selectedTower.id][0][data.selectedTower.upgrade1]
                    data.selectedTower.upgrade1 += 1
                if i==1 and data.selectedTower.upgrade2 < 5 and data.gold >= data.tower_upgrade_costs[data.selectedTower.id][1][data.selectedTower.upgrade2]:
                    data.gold -= data.tower_upgrade_costs[data.selectedTower.id][1][data.selectedTower.upgrade2]
                    data.selectedTower.upgrade2 += 1
                if i==2 and data.selectedTower.upgrade3 < 5 and data.gold >= data.tower_upgrade_costs[data.selectedTower.id][2][data.selectedTower.upgrade3]:
                    data.gold -= data.tower_upgrade_costs[data.selectedTower.id][2][data.selectedTower.upgrade3]
                    data.selectedTower.upgrade3 += 1
        return

    # Check if clicked buying menu
    if mouse_x > 1175:
        data.select = None
        for y in range(0,6):
            for x in range(0,2):
                if mouse_x > 75 * x + 1180 and mouse_x < 75 * x + 1180 + 75 and mouse_y > 90 * y + 115 and mouse_y < 90 * y + 115 + 90:
                    data.select = y * 2 + x
                    data.placing_tower = True
                    return




    # Check if clicked tower
    for i in data.towers:
        if mouse_x > i.x and mouse_x < i.x + data.towers_png[i.id].get_size()[0] and mouse_y > i.y and mouse_y < i.y + data.towers_png[i.id].get_size()[1]:
            data.show_tower_menu = True
            data.selectedTower = i
            return
    data.show_tower_menu = False


def on_right_click():
    if data.placing_tower:
        data.placing_tower = False