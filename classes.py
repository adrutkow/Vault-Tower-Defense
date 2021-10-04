import data
from random import randint
import math
import class_functions
import pygame


class Bloon:
    def __init__(self, level, x=10, y=data.screen_height/2):
        self.screen = data.screen
        self.x = x
        self.y = y
        self.level = level
        self.hp = data.bloon_hp[level]
        self.offset = (data.bloons_png[level].get_size()[0]/2, data.bloons_png[level].get_size()[1]/2)
        self.size = data.bloons_png[level].get_size()[0]
        self.gold = level
        self.gusd = False
        self.gusdTimer = 0
        self.abnor = False
        self.abnorTimer = 0

    def draw(self):
        class_functions.draw_bloon(self)

    def tick(self):
        class_functions.tick_bloon(self)


class Tower:
    def __init__(self, id):
        self.id = id
        self.x = pygame.mouse.get_pos()[0] - int(data.towers_png[data.select].get_size()[0]/2)
        self.y = pygame.mouse.get_pos()[1] - int(data.towers_png[data.select].get_size()[1]/2)
        self.range = data.tower_stats[id][1]
        self.attackSpeed = data.tower_stats[id][3]
        self.projectileSpeed = data.tower_stats[id][4]
        self.damage = data.tower_stats[id][2]
        self.timer = 0
        test = (tuple(int(i/2) for i in data.towers_png[self.id].get_size()))
        self.offset = (test[0] + self.x,test[1] + self.y)
        self.bonusDamage = 0
        self.bonusRange = 0
        self.pops = 0
        self.buffed = False
        self.buffOwner = None
        self.buffTimer = 0
        self.upgrade1 = 1
        self.upgrade2 = 1
        self.upgrade3 = 1
        self.currentRange = 0
        self.currentDamage = 0
        self.currentProjectileSpeed = 0
        self.currentAttackSpeed = 0

    def draw(self):
        class_functions.draw_tower(self)


    def shoot(self):
        class_functions.tower_shoot(self)

    def tick(self):
        self.timer += 1
        self.shoot()
        self.draw()


class Trap:
    def __init__(self, x, y, lifespan, hp, damage, owner):
        self.x = x
        self.y = y
        self.lifespan = lifespan
        self.hp = hp
        self.damage = damage
        self.owner = owner
        self.timer = 0

    def draw(self):
        class_functions.draw_trap(self)

    def tick(self):
        class_functions.tick_trap(self)

class Projectile:
    def __init__(self, x, y, damage, speed, image, angle, owner, maxLifetime=300):
        self.x = x
        self.y = y
        self.damage = damage
        self.speed = speed
        self.image = image
        self.angle = angle
        self.offset = (tuple(int(i/2) for i in self.image.get_size()))
        self.owner = owner
        self.lifetime = 0
        self.maxLifetime = maxLifetime
        if self.owner.id == 11:
            self.maxLifetime = 10

    def draw(self):
        class_functions.draw_projectile(self)

    def is_colliding(self):
        class_functions.is_projectile_colliding(self)

    def tick(self):
        self.lifetime += 1
        if self.lifetime > self.maxLifetime:
            data.projectiles.remove(self)
            del self
            return
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.is_colliding()
        self.draw()


class Spawner:
    def __init__(self):
        self.x = 0
        self.y = data.screen_height / 2
        self.cooldown = 10
        self.timer = 0
        self.roundHp = 10

    def check_max(self):
        for i in range(0,12):
            if 2**i+1 > self.roundHp:
                return i
        return 11

    def spawn_bloon(self, level):
        data.bloons.append(Bloon(level))

    def tick(self):

        if data.round == 0:
            return

        self.timer -= 1
        if self.timer <= 0:
            if self.roundHp > 0:
                next_bloon = randint(0, self.check_max())
                self.roundHp -= 2**next_bloon+1
                self.spawn_bloon(next_bloon)
                self.timer = randint(1,30)
            if self.roundHp <= 0 and len(data.bloons) == 0 and data.health > 0:
                data.round += 1
                data.gold += 50 + int(data.round/2)
                self.timer = 10
                self.roundHp = data.round * 5 + randint(0,10)


class Despawner:
    def __init__(self):
        self.x = data.screen_width
        self.y = data.screen_height / 2

    def tick(self):
        for i in data.bloons:
            if i.x > self.x:
                data.health -= i.hp + 1
                data.bloons.remove(i)
                del i

class Obstacle:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2