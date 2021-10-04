import pygame

screen_width = 1366
screen_height = 768
screen = pygame.display.set_mode([1366, 768])
towerCount = 12
bloonCount = 12
bg = pygame.image.load("files/XD.png")
menu = pygame.image.load("files/menu.png")
buff_icon = pygame.image.load("files/buff_icon.png")
tower_menu = pygame.image.load("files/tower_menu.png")
health_gold = pygame.image.load("files/health_gold.png")
abnor = pygame.image.load("files/abnor.png")
clock = pygame.time.Clock()
fps = 60
health = 100
gold = 850
bloons_png = []
towers_png = []
projectiles_png = []
obstacles = []
bloons = []
towers = []
spawners = []
cheat_code = ""
projectiles = []
traps = []
despawners = []
show_tower_menu = False
placing_tower = False
select = 0
selectedTower = None
round = 0

for i in range(0, bloonCount):
    bloons_png.append(pygame.image.load("files/bloon_" + str(i) + ".png"))

for i in range(0, towerCount):
    towers_png.append(pygame.image.load("files/tower_" + str(i) + ".png"))

for i in range(0, towerCount):
    projectiles_png.append(pygame.image.load("files/projectile_" + str(i) + ".png"))

pygame.display.set_icon(towers_png[9])
pygame.display.set_caption("Vault Tower Defense")
# (cost, range, damage, attackSpeed, projectileSpeed)

bloon_hp = (1,1,1,1,1,1,1,100,400,700,3000,6000)
bloon_children = ((),(0,2),(1,2),(2,2),(3,2),(4,2),(5,2),(6,4),(7,4),(8,4),(9,4),(10,4))

tower_stats = ((300, 150, 1, 50, 10), (600, 100, 3, 150, 500), (1200, 30, 5, 300, 7), (1500, 200, 1, 150, 100), (3500, 2000, 1, 200, 20),(800, 350, 5, 20, 50),
               (9999999, 2000, 9999, 1, 50),(1,1,-2,1000,1),(5000,175,1,50,50),(3000,175,20,45,15),(1234,200,10,100,45),(15000,200,1,45,50))
tower_names = ("DubstepCatOwO","Salt factory","Slav","Speed","Glebu","Spood","Goga","Ajeaje","Abnormal","Sims 4 Noze","Mysterious man","Bloodedge the Minion")
tower_upgrade_names = ((("cat bombs","yasuo bombs","globox bombs","dubstep bombs","rayman bombs"),
                       ("fast bombs","very fast bombs","epicly fast bombs","lethal tempo bombs","spastic bombs"),
                       ("funny range","very funny range","epic range","ultra range","XD range")),

                       (("bad salt","toxic salt","cancer salt","league salt","unnatural salt"),
                        ("fast salt","very fast salt","epicly fast salt","super pooper salt","infinite salt"),
                        ("long lasting salt","very long lasting salt","wow","epic","permasalt")),

                       (("millionaire grindset","billionaire grindset","trillionaire grindset","octimillionaire grindset","never stopping grindset"),
                        ("fast working","fast grinding","hired help","slaving children","children factory"),
                        ("family","family","family","family","family")),

                       (("more bonus damage","even more bonus damage","epic bonus damage","super duper bonus damage","support main"),
                       ("faster support","even faster support","epic fast support","ultra fast support","permasupport"),
                        ("big range","bigger range","epic range","super duper ranger","infinirange")),

                       (("mr white","i need","12 km/h of meth","now","gus"),
                       ("walter white","i will kill","your infant daughter","lmaoo","dies"),
                       ("meth production","super meth production","children slavery","children killing","turning children into meth")),

                       (("fast shooting","very fast shooting","automatic rifle","machine gun","lethal tempo irl"),
                        ("more damage","AP ammo","heavy ammo","epic ammo","god ammo"),
                        ("bigger range","epic range","ultra range","awesome range","infini range")),

                       (("goga","goga","goga","goga","goga"),
                       ("goga", "goga", "goga", "goga", "goga"),
                       ("goga", "goga", "goga", "goga", "goga")),

                       (("ajeaje","ajeaje","ajeaje","ajeaje","ajeaje"),
                       ("ajeaje", "ajeaje", "ajeaje", "ajeaje", "ajeaje"),
                       ("ajeaje", "ajeaje", "ajeaje", "ajeaje", "ajeaje")),

                       (("slow", "more slow", "epic slow", "singed W", "nasus' wither"),
                        ("range", "more range", "epic range", "super range", "infini range"),
                        ("poison", "super poison", "singed Q", "league reference lmaoo", "epic poison")),

                       (("noze damage", "more noze damage", "epic noze damage", "noze gang", "noze god"),
                        ("fast noze", "faster noze", "super fast noze", "ultra fast noze", "lightspeed noze"),
                        ("noze range", "noze super range", "noze epic range", "noze ultra range", "noze infini range")),

                       (("box damage", "epic box damage", "troll box damage", "XD box damage", "box"),
                        ("fast box", "faster box", "i ran out of ideas", "ultra box", "it isnt lore accurate"),
                        ("range", "more range", "we get it", "even more range", "epic range lol lmao")),

                       (("bloodedge blade", "trol", "lmao", "xd", "im so done with this"),
                        ("im so tired", "XD", "lmao", "no one will read this", "trol"),
                        ("hahaha!!", "LMAOO", "ROFL", "XDDD", "ok")))


tower_upgrade_descriptions = (("more damaging bombs","faster bombs","more range"),
                              ("salt does more damage","faster salt throwing","salt has a longer lifespan"),
                              ("more money generation","faster money generation","generates more health per round"),
                              ("gives more damage to nearby towers","gives support faster to nearby towers","bigger support range"),
                              ("more knockback","faster knockback","produces meth, which literally does nothing"),
                              ("shoots faster","shots do more damage","more range"),
                              ("goga","goga","goga"),
                              ("hospital", "ajeaje", "none of these upgrade do anything"),
                              ("slows more", "more range", "slow poisons aswell"),
                              ("more damage", "more attack speed", "more range"),
                              ("more damage", "more attack speed", "more range"),
                              ("the more kills he has, the more damage he deals","more attack speed","more range"))

tower_upgrade_costs = (((300,150,300,500,800),(500,900,1500,3000,5000),(500,1000,1500,3000,5000)),
                        ((300,600,900,1500,4000),(500,900,1500,3000,5000),(500,1000,1500,3000,5000)),
                       ((300, 600, 900, 1500, 4000), (500, 900, 1500, 3000, 5000), (500, 1000, 1500, 3000, 5000)),
                       ((300, 600, 900, 1500, 4000), (500, 900, 1500, 3000, 5000), (500, 1000, 1500, 3000, 5000)),
                       ((300, 600, 900, 1500, 4000), (500, 900, 1500, 3000, 5000), (500, 1000, 1500, 3000, 5000)),
                       ((300, 600, 900, 1500, 4000), (500, 900, 1500, 3000, 5000), (500, 1000, 1500, 3000, 5000)),
                       ((300, 600, 900, 1500, 4000), (500, 900, 1500, 3000, 5000), (500, 1000, 1500, 3000, 5000)),
                       ((300, 600, 900, 1500, 4000), (500, 900, 1500, 3000, 5000), (500, 1000, 1500, 3000, 5000)),
                       ((300, 600, 900, 1500, 4000), (500, 900, 1500, 3000, 5000), (500, 1000, 1500, 3000, 5000)),
                       ((300, 600, 900, 1500, 4000), (500, 900, 1500, 3000, 5000), (500, 1000, 1500, 3000, 5000)),
                       ((300, 600, 900, 1500, 4000), (500, 900, 1500, 3000, 5000), (500, 1000, 1500, 3000, 5000)),
                       ((300, 600, 900, 1500, 4000), (500, 900, 1500, 3000, 5000), (500, 1000, 1500, 3000, 5000)))
