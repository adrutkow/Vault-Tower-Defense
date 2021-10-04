import pygame
import functions
import data
import classes
from random import randint

def draw_tower(self):
    data.screen.blit(data.towers_png[self.id], (self.x, self.y))
    if self.id == 5:
        test = functions.is_bloon_in_range(self)
        if test is not False:
            pygame.draw.line(data.screen, (255, 0, 0), self.offset, (test.x, test.y))


def draw_bloon(self):
    if self.level < 0:
        self.level = 0
    data.screen.blit(data.bloons_png[self.level], (self.x - self.offset[0], self.y - self.offset[1]))
    if self.abnor:
        data.screen.blit(data.abnor, (self.x, self.y))


def draw_trap(self):
    data.screen.blit(data.projectiles_png[1], (self.x, self.y))


def draw_projectile(self):
    data.screen.blit(self.image, (self.x - self.offset[0], self.y - self.offset[1]))


def tick_bloon(self):
    global gold
    if self.hp < 0:
        data.bloons.remove(self)
        data.gold += self.gold + 1
        del self
        return

    if self.abnor:
        self.abnorTimer -= 1
        if self.abnorTimer <= 0:
            self.abnor = False
            self.abnorTimer = 0

    if self.gusd:
        self.gusdTimer += 1
        self.x -= 5
        if self.x < 0:
            self.x == 0
        if self.gusdTimer > 30:
            self.gusd = False
            self.gusdTimer = 0
    else:
        debuff = 0
        if self.level > 6:
            debuff = int(self.level / 2)
        currentSpeed = 1 + self.level / 2 - debuff
        if self.abnor:
            currentSpeed = currentSpeed / 2
        self.x += currentSpeed
    self.draw()


def tick_trap(self):
    self.timer += 1
    if self.timer > self.lifespan:
        data.traps.remove(self)
        del self
        return
    self.draw()
    for i in data.bloons:
        if functions.distance(self.x, i.x, self.y, i.y) < 15:
            functions.damage_bloon(i, self)

    if self.damage <= 0:
        data.traps.remove(self)
        del self

def tower_shoot(self):

    self.currentDamage = self.damage + self.bonusDamage
    self.currentRange = self.range + self.bonusRange
    self.currentAttackSpeed = self.attackSpeed
    self.currentProjectileSpeed = self.projectileSpeed

    if self.buffOwner == None:
        self.buffed = False

    if self.buffed:
        self.buffTimer -= 1
        self.currentDamage += self.buffOwner.upgrade1 * 2
        self.currentRange += self.buffOwner.upgrade3 * 15

        if self.buffTimer <= 0:
            self.buffed = False
            self.buffTimer = 0
            self.buffOwner = None

    # Cat bonuses
    if self.id == 0:
        self.currentDamage += self.upgrade1 * 3
        if self.upgrade1 == 5:
            self.currentDamage += 15

        self.currentAttackSpeed -= self.upgrade2 * 5
        if self.upgrade2 == 5:
            self.currentAttackSpeed -= 3

        self.currentProjectileSpeed += self.upgrade2 * 2

        self.currentRange += self.upgrade3 * 50
        if self.upgrade3 == 5:
            self.currentRange += 200

    # Salt bonuses
    if self.id == 1:
        self.currentDamage += self.upgrade1 * 4
        if self.upgrade1 == 5:
            self.currentDamage += 3

        self.currentAttackSpeed -= self.upgrade2 * 5
        if self.upgrade2 == 5:
            self.currentAttackSpeed -= 20

        self.currentProjectileSpeed += self.upgrade2 * 20
        if self.upgrade3 == 5:
            self.currentProjectileSpeed = 2000

    # Slav bonuses
    if self.id == 2:
        self.currentDamage += self.upgrade1 * 20
        if self.upgrade1 == 5:
            self.currentDamage += 100

        self.currentAttackSpeed -= self.upgrade2 * 2
        if self.upgrade2 == 5:
            self.currentAttackSpeed -= 3

    # Speed bonuses
    if self.id == 3:
        self.currentDamage += self.upgrade1 * 1
        if self.upgrade1 == 5:
            self.currentDamage += 2

        self.currentAttackSpeed -= self.upgrade2 * 2
        if self.upgrade2 == 5:
            self.currentAttackSpeed -= 3

        self.currentRange += self.upgrade3 * 75

    # Glebu bonuses
    if self.id == 4:
        self.currentDamage += self.upgrade1 * 1
        if self.upgrade1 == 5:
            self.currentDamage += 2

        self.currentAttackSpeed -= self.upgrade2 * 2
        if self.upgrade2 == 5:
            self.currentAttackSpeed -= 3

    # Spood bonuses
    if self.id == 5:
        self.currentDamage += self.upgrade2 * 1
        if self.upgrade2 == 5:
            self.currentDamage += 2

        self.currentAttackSpeed -= self.upgrade1 * 2
        if self.upgrade1 == 5:
            self.currentAttackSpeed -= 5

        self.currentRange += self.upgrade3 * 50
        if self.upgrade3 == 5:
            self.currentRange = 2000

    # Abnormal bonuses
    if self.id == 8:
        self.currentRange += self.upgrade2 * 100
        self.projectileSpeed += self.upgrade1 * 10

    # Noze bonuses
    if self.id == 9:
        self.currentDamage += self.upgrade1 * 10
        self.currentRange += self.upgrade3 * 100
        self.currentAttackSpeed -= self.upgrade2 * 3
        if self.upgrade3 == 5:
            self.currentRange += 2000

    # Mysterious man bonuses
    if self.id == 10:
        self.currentDamage += self.upgrade1 * 10
        self.currentRange += self.upgrade3 * 100
        self.currentAttackSpeed -= self.upgrade2 * 3

    # Bloodedge the minion bonuses
    if self.id == 11:
        self.currentDamage += 1 + int(self.pops) / 10000 * (self.upgrade1 * 10)
        self.currentRange += self.upgrade3 * 50
        self.currentAttackSpeed -= self.upgrade2 * 4
        if self.upgrade2 == 5:
            self.currentAttackSpeed += 10

    if data.show_tower_menu and data.selectedTower == self:
        functions.draw_text("Damage: " + str(self.currentDamage), 0, 650, 25, (255, 0, 0))
        functions.draw_text("Attack Speed: " + str(1 / self.currentAttackSpeed * 60)[0:4] + "/s ("+str(self.currentAttackSpeed)+")", 0, 675, 25, (255, 0, 0))
        functions.draw_text("Range: " + str(self.currentRange), 0, 700, 25, (255, 0, 0))

    if self.timer >= self.currentAttackSpeed:
        self.timer = 0
        if self.id == 1:
            functions.add_trap(self.x - 100 + randint(0, 200), 380, self.currentProjectileSpeed, 5, self.currentDamage, self)
        elif self.id == 2:
            data.gold += self.currentDamage
            self.pops += self.currentDamage
            data.health += self.upgrade3 * 3
            if data.health > 1000:
                data.health = 1000
        elif self.id == 3:
            for i in data.towers:
                if i is self:
                    continue
                if functions.distance(self.x, i.x, self.y, i.y) <= self.range and i.buffed == False:
                    i.buffed = True
                    i.buffTimer = self.upgrade2 * 150
                    i.buffOwner = self
                    break
        elif self.id == 4:

            list = []
            for b in data.bloons:
                list.append(b)
            for b in list:
                b.gusd = True
                temp = classes.Projectile(0, 0, self.currentDamage, 0, data.projectiles_png[self.id], 0, self)
                functions.damage_bloon(b, temp)

        elif self.id == 8:
            for i in data.bloons:
                if i.abnor:
                    functions.damage_bloon(i, classes.Projectile(0,0,self.currentDamage, 0, data.projectiles_png[4], 0, self))
                if functions.is_bloon_in_range(self, i):
                    i.abnor = True
                    i.abnorTimer = self.projectileSpeed


        else:
            test = functions.is_bloon_in_range(self)
            if test is not False:
                angle = functions.get_angle(self.offset[0], self.offset[1], test.x + 5, test.y)
                data.projectiles.append(
                    classes.Projectile(self.offset[0], self.offset[1], self.currentDamage, self.currentProjectileSpeed,
                               data.projectiles_png[self.id], angle, self))


def is_projectile_colliding(self):
    for i in data.bloons:
        if functions.distance(self.x + self.offset[0], i.x + i.offset[0], self.y + self.offset[1], i.y + i.offset[1]) < i.size:
            if self.owner.id == 4:
                i.gusd = True
            # while self.damage > 0 and i.hp >= 0:
            #     self.damage -= 1
            #     self.owner.pops += 1
            #     i.hp -= 1
            #     i.level = i.hp

            functions.damage_bloon(i, self)

            if self.damage == 0:
                data.projectiles.remove(self)
                del self
                return