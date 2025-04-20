from django.db import models
import random
from django.contrib.auth.models import User


# CHOICES MODELS


# Bonus (Discrete, Athletic, Aimbot, Powerful, Charming, Focused, Biologist, Technician)
class Bonus(models.TextChoices):
    DISCRETE = "Discrete"
    ATHLETIC = "Athletic"
    AIMBOT = "Aimbot"
    POWERFUL = "Powerful"
    CHARMING = "Charming"
    FOCUSED = "Focused"
    BIOLOGIST = "Biologist"
    TECHNICIAN = "Technician"
    NONE = "none"

# Malus (Loud, Asthmatic, Four eyes, Weak, Ugly, Careless, Complotist, Clumsy)
class Malus(models.TextChoices):
    LOUD = "Loud"
    ASTHMATIC = "Asthmatic"
    FOUREYES = "Four Eyes"
    WEAK = "Weak"
    UGLY = "Ugly"
    CARELESS = "Careless"
    COMPLOTIST = "Complotist"
    CLUMSY = "Clumsy"
    NONE = "none"

# Points - body & mind (min : 1, max : 4)
class Points(models.IntegerChoices):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4

# Power - threat level from events
class Power(models.IntegerChoices):
    ONE = 1
    TWO = 2
    THREE = 4
    FOUR = 6
    FIVE = 8
    SIX = 10

# Category - type of event (Monster, Menace, Finding, Recrute, Survivors,...)
class Category(models.TextChoices):
    MENACE = "menace"
    MONSTER = "monster"
    SURVIVORS = "survivors"
    FINDING = "finding"
    MOTORS = "motors"
    ANIMALS = "animals"
    RECRUTE = "recrute"
    NONE = "none"

# Type - type of rewards, losses (resources,survivors,hp,...)
class Type(models.TextChoices):
    HP = "hp"
    COINS = "coins"
    SURVIVORS = "survivor"
    DRUGS = "drug"
    MEDS = "med"
    ARMORS = "armor"
    KATANAS = "katana"
    SHOTGUNS = "shotgun"
    IMPLANT = "implant"
    FOOD = "food"
    WOOD = "wood"
    METAL = "metal"
    FUEL = "fuel"
    MOTORS = "motors"
    ANIMALS = "animals"
    UNKNOWN = "unknown"
    PP = "plan's part"
    BANDAGE = "bandage"
    CURE = "cure"
    RECRUTE = "recrute"
    NONE = "none"


# MODELS


# Inventory - every region and character has it own inventory
class Inventory(models.Model):
    food = models.IntegerField(default=0)
    wood = models.IntegerField(default=0)
    metal = models.IntegerField(default=0)
    fuel = models.IntegerField(default=0)
    bandage = models.IntegerField(default=0)
    med = models.IntegerField(default=0)
    drug = models.IntegerField(default=0)
    armor = models.IntegerField(default=0)
    implant = models.IntegerField(default=0)
    katana = models.IntegerField(default=0)
    shotgun = models.IntegerField(default=0)
    coins = models.IntegerField(default=0)
    pp = models.IntegerField(default=0)
    cure = models.IntegerField(default=0)
    limit = models.BooleanField(default=False)

    def loot(self):
        pass

# Region - regions are places to explore, where players can farm and build
class Region(models.Model):
    rinv = models.OneToOneField(
        Inventory,
        on_delete=models.CASCADE,
        primary_key= True,
    )
    founder = models.CharField(default="none")
    name = models.CharField(default="none")
    druguse = models.BooleanField(default=True)
    prostitution = models.BooleanField(default=True)
    allegiance = models.TextField(default="none")
    x = models.IntegerField()
    y = models.IntegerField()
    biome = models.CharField(default="")
    color = models.CharField(default="black")
    landscape = models.ImageField()
    visited = models.BooleanField(default=False)
    discovered = models.BooleanField(default=False)
    build = models.BooleanField(default=True)
    farm = models.BooleanField(default=True)
    leader = models.BooleanField(default=False)
    leadport = models.ImageField()
    merchant = models.BooleanField(default=False)
    mercport = models.ImageField()
    doctor = models.BooleanField(default=False)
    docport = models.ImageField()
    dealer = models.BooleanField(default=False)
    dealport = models.ImageField()
    mecano = models.BooleanField(default=False)
    mecaport = models.ImageField()
    workers = models.IntegerField(default=0)
    survivors = models.IntegerField(default=0)
    fo = models.IntegerField(default=0)
    wo = models.IntegerField(default=0)
    me = models.IntegerField(default=0)
    fu = models.IntegerField(default=0)

    # generate 50x50 new region objects with x and y coordinates
    def world():
        a = 1
        b = 1
        while a < 51 and b < 51:
            if a == 25 and b == 25 :
                i = Inventory()
                i.food = 1000
                i.wood = 1000
                i.metal = 1000
                i.fuel = 1000
                i.bandage = 500
                i.med = 500
                i.drug = 500
                i.armor = 50
                i.implant = 0
                i.katana = 100
                i.shotgun = 100
                i.coins = 10000
                i.pp = 0
                i.cure = 0
                i.limit = False
                i.save()
                r = Region()
                r.rinv = i
                r.x = a
                r.y = b
                r.biome = "Spawn"
                r.discovered = True
                r.visited = True
                r.name = "Prosperity"
                r.landscape = "spawn.jpg"
                r.leader = True
                r.leadport = "leader.jpg"
                r.doctor = True
                r.docport = "doctor.jpg"
                r.merchant = True
                r.mercport = "merchant.jpg"
                r.dealer = True
                r.dealport = "dealer.jpg"
                r.mecano = True
                r.mecaport = "mecano.jpg"
                r.survivors = 1000
                r.farm = False
                r.build = False
                r.color = "orange"
                r.save()
                a += 1
            else :
                i = Inventory()
                i.save()
                r = Region(rinv=i,x=a,y=b,biome="",visited=False)
                r.save()
                a += 1
                if a == 51:
                    b += 1
                    a = 1
                else :
                    continue

    # generate random amount of resources    
    def resources(x,y):
        return random.randint(x,y)

    # add survivors to camp/shelter/fortress depending on a lot of parameters
    def populate(self):
        if self.survivors >= 50 :
            self.survivors += 2
        elif self.survivors >= 100 :
            self.survivors += 5
        elif self.survivors >= 250 :
            self.survivors += 10
        elif self.survivors >= 500 :
            self.survivors += 20
        else :
            pass

    # add or remove survivors from work
    def work(self,player,wlist):
        n = 1
        food = ["Plain","Aquatic","Forest","Mountain"]
        wood = ["Forest","Plain","Mountain"]
        fuel = ["Desert","Aquatic"]
        for res in wlist :
            if n == 1 and self.checkres("food"):
                self.fo += int(res)
                n += 1
            elif n == 2 and self.checkres("wood"):
                self.wo += int(res)
                n += 1
            elif n == 3 and "Mountain" in self.checkres():
                self.me += int(res)
                n += 1
            elif n == 4 and self.checkres("fuel"):
                self.fu += int(res)
                n += 1
            else :
                player.journal = { 'entry' : "this resource is unavalaible"}
        workers = self.fo + self.wo + self.me + self.fu
        if workers <= self.survivors :
            self.save()
        else :
            player.journal = { 'entry' : "not enough work force !"}

    # resources regrowth of natural regions
    def autores():
        world = Region.objects.all()

        for r in world :
            if r.biome != "Camp" or r.biome != "Shelter" or r.biome != "Fortress" :
                inv = Inventory.objects.get(pk=r.pk)
                if r.discovered :
                    if r.biome == "Aquatic":
                        inv.food += 2
                        inv.fuel += 1
                        inv.save()
                    elif r.biome == "Desert":
                        inv.fuel += 2
                        inv.save()
                    elif r.biome == "Mountain":
                        inv.food += 1
                        inv.wood += 1
                        inv.metal += 2
                        inv.save()
                    elif r.biome == "Forest":
                        inv.food += 1
                        inv.wood += 3
                        inv.save()
                    else :
                        inv.food += 3
                        inv.wood += 1
                        inv.save()
                else :
                    continue
            else :
                continue

    # activate the workers production
    def working(self):
        inventory = Inventory.objects.get(pk=self.pk)

        inventory.food += self.fo * 3
        inventory.food -= self.survivors
        inventory.wood += self.wo * 2
        inventory.wood -= self.survivors
        inventory.metal += self.me
        inventory.fu += self.fu
        inventory.save()

        print("it's working...")

    # create a list of all regions in a radius around the designated region
    def scan(self):
        x = self.x
        y = self.y
        a = x-2
        b = y-2
        sector = []
        while a <= x+2 and b <= y+2 :
            print("holyshit")
            sector.append(Region.objects.get(x=a,y=b))
            a += 1
            if a == x+2 :
                a = x-2
                b += 1
                sector.append(Region.objects.get(x=a,y=b))
            else :
                continue
        return sector

    # check if a scanned sector contains biomes or not
    def checkres(self, type):
        sector = self.scan()
        rfood = ["Plain","Mountain","Aquatic","Forest"]
        rwood = ["Plain","Mountain","Forest"]
        rfuel = ["Aquatic","Desert"]
        for s in sector :
            if type == "food" :
                if s in rfood :
                    return True
                else :
                    return False
            elif type == "wood" :
                if s in rwood :
                    return True
                else :
                    return False
            else :
                if s in rfuel :
                    return True
                else :
                    return False

    # generate all resources of a region when it's discovered
    def res(region,bio):
        if bio == "Desert" :
            region.food = 0
            region.wood = 0
            region.metal = 0
            region.fuel = Region.resources(1000,5000)
        elif bio == "Aquatic" :
            region.food = Region.resources(1000,5000)
            region.wood = 0
            region.metal = 0
            region.fuel = 0
        elif bio == "Mountain" :
            region.food = Region.resources(500,1000)
            region.wood = Region.resources(500,2500)
            region.metal = Region.resources(1000,5000)
            region.fuel = 0
        elif bio == "Forest" :
            region.food = Region.resources(500,2500)
            region.wood = Region.resources(1000,5000)
            region.metal = 0
            region.fuel = 0
        else :
            region.food = Region.resources(1000,5000)
            region.wood = Region.resources(500,2500)
            region.metal = 0
            region.fuel = 0
        region.save()

    # check if a scanned sector contains spawn, camp, shelter or fortress
    def checkbuild(self) :
        print("checkbuild function starting...")
        x = self.x
        a = 5
        b = 5
        y = self.y
        bio = []
        while a >= -5 :
            self.x = x + a
            newr = Region.objects.get(x=self.x,y=self.y)
            print(newr.x,newr.y)
            bio.append(newr.biome)
            a -= 1
            if a == -6 :
                while b >= -5 :
                    self.y = y + b
                    newr = Region.objects.get(x=self.x,y=self.y)
                    print(newr.x,newr.y)
                    bio.append(newr.biome)
                    b -= 1
                    a = 5
            else :
                continue
        print(bio)
        if "Spawn" in bio or "Camp" in bio or "Shelter" in bio or "Fortress" in bio :
            return True
        else :
            return False

    # check if the player is the founder's region
    def checkfounder(player):
        print("checkfounder function starting...")
        world = Region.objects.all()
        for r in world :
            if r.founder == player.name :
                print(r.founder, player.name)
                return True
            else :
                print(r.founder)
                return False
            
# Player - for players and npc ( non player characters )
class Player(models.Model):
    pinv = models.OneToOneField(
        Inventory,
        on_delete=models.CASCADE,primary_key= True,
    )
    name = models.CharField(max_length=20)
    avatar = models.ImageField(default='member.jpg', blank=True)
    x = models.IntegerField(default=2500)
    y = models.IntegerField(default=2500)
    body = models.IntegerField(default=0,choices=Points.choices)
    mind = models.IntegerField(default=0,choices=Points.choices)
    bonus1 = models.TextField(default="none",choices=Bonus.choices)
    bonus2 = models.TextField(default="none",choices=Bonus.choices)
    malus1 = models.TextField(default="none",choices=Malus.choices)
    malus2 = models.TextField(default="none",choices=Malus.choices)
    hp = models.IntegerField(default=5)
    maxhp = models.IntegerField(default=7)
    melee = models.IntegerField(default=1)
    dist = models.IntegerField(default=1)
    aim = models.IntegerField(default=2)
    speed = models.IntegerField(default=1)
    armor = models.IntegerField(default=0)
    range = models.IntegerField(default=1)
    sick = models.BooleanField(default=False)
    trauma = models.BooleanField(default=False)
    tired = models.BooleanField(default=False)
    wound = models.BooleanField(default=False)
    katana = models.BooleanField(default=False)
    shotgun = models.BooleanField(default=False)
    occupied = models.CharField(default="free")
    surv = models.IntegerField(default=0)
    move = models.CharField(default="foot")
    group = models.JSONField(default=dict)
    shelters = models.JSONField(default=dict)
    journal = models.TextField(default="journal infos")
    countdown = models.IntegerField(default=0)
    distance = models.IntegerField(default=0)
    luck = models.IntegerField(default=0)
    start = models.BooleanField(default=True)
    turn = models.BooleanField(default=False)
    selected = models.BooleanField(default=False)
    action = models.CharField(default="none")

    # verify if the player and his party can do the travel or not
    def travel(self,player,party,inventory,a,b,x,y):

        r = party.checkrobot(party,player)
        food = party.countmember() - r+1
        fo = food / 2
        fuel = r

        print("calculating travel possibility...")
        if player.tired :
            player.journal = "you're too tired to travel !"
            player.save()
            return False
        else :
            if player.move == "foot" :
                c = a + 1
                d = b + 1
                e = a - 1
                f = b - 1
                if x <= c and x >= e and y <= d and y >= f :
                    if inventory.food >= food :
                        inventory.food -= food
                        inventory.fuel -= r
                        inventory.save()
                        return True
                    else :
                        player.journal = "not enough food"
                        player.save()
                        return False
                else :
                    return False
            elif player.move == "horse" :
                c = a + 2
                d = b + 2
                e = a - 2
                f = b - 2
                if x <= c and x >= e and y <= d and y >= f :
                    if inventory.fuel >= r and inventory.food >= fo :
                        inventory.fuel -= r
                        inventory.food -= fo
                        inventory.save()
                        return True
                    else :
                        player.journal = "not enough food"
                        return False
                else :
                    return False
            else :
                c = a + 3
                d = b + 3
                e = a - 3
                f = b - 3
                if x <= c and x >= e and y <= d and y >= f :
                    if inventory.fuel >= 2 and inventory.food >= fo :
                        inventory.fuel -= 2
                        inventory.food -= fo
                        inventory.save()
                        return True
                    else :
                        player.journal = "not enough fuel"
                        return False
                else :
                    return False

    # add a new member to the player's party
    def recrute(self,name,party):
        event = Event.objects.get(name=self.occupied)
        i = Inventory()
        i.save()
        npc = Player()
        npc.pinv = i
        npc.avatar = event.illus

        if name == "robot":
            i.armor = 1
            npc.name = name
            npc.body = 3
            npc.mind = 3
            npc.bonus1 = "Biologist"
            npc.malus1 = "Loud"
        elif name == "bounty" :
            i.shotgun = 1
            npc.name = name
            npc.body = 3
            npc.mind = 2
            npc.bonus1 = "Aimbot"
            npc.malus1 = "Ugly"
        elif name == "mercenary" :
            i.katana = 1
            npc.name = name
            npc.body = 4
            npc.mind = 1
            npc.bonus1 = "Athletic"
            npc.malus1 = "Complotist"
        elif name == "queen" :
            npc.name = name
            npc.hp = 10
            npc.armor = 2
            npc.body = 4
            npc.mind = 1
            npc.bonus1 = "Powerful"
            npc.malus1 = "Loud"
        elif name == "horse" :
            npc.name = name
            npc.hp = 5
            npc.body = 3
            npc.mind = 1
            npc.bonus1 = "Athletic"
        elif name == "dog" :
            npc.name = name
            npc.hp = 3
            npc.body = 2
            npc.mind = 2
            npc.bonus1 = "Focus"
        else :
            npc.name = name
            npc.hp = 3
            npc.body = 2
            npc.mind = 2
            npc.bonus1 = "Charming"

        if party.mem2 == 0 :
            party.mem2 = npc.pk
            i.save()
            npc.save()
            party.save()
        elif party.mem3 == 0 :
            party.mem3 = npc.pk
            i.save()
            npc.save()
            party.save()
        elif party.mem4 == 0 :
            party.mem4 = npc.pk
            i.save()
            npc.save()
            party.save()
        elif party.mem5 == 0 :
            party.mem5 = npc.pk
            i.save()
            npc.save()
            party.save()
        elif party.mem6 == 0 :
            party.mem6 = npc.pk
            i.save()
            npc.save()
            party.save()
        elif party.mem7 == 0 :
            party.mem7 = npc.pk
            i.save()
            npc.save()
            party.save()
        else :
            self.journal = { 'entry' : "party is already full..." }
            pass

    # allow the player to use and equip items
    def use(char,inventory,party,r) :
        if r == "🩸" :
            if inventory.bandage > 0 :
                inventory.bandage -= 1
                char.wound = False
            elif inventory.cure > 0 :
                inventory.cure -= 1
                char.wound = False
            else :
                pass
        elif r == "🤢" :
            if inventory.med > 0 :
                inventory.med -= 1
                char.wound = False
            elif inventory.cure > 0 :
                inventory.cure -= 1
                char.wound = False
            else :
                pass
        elif r == "😨" :
            if inventory.drug > 0 :
                inventory.drug -= 1
                char.wound = False
            elif inventory.cure > 0 :
                inventory.cure -= 1
                char.wound = False
            else :
                pass
        elif r == "1" or r == "0" :
            if inventory.armor > 0 :
                inventory.armor -= 1
                char.armor += 1
            else :
                pass
        elif r == "👊" :
            if inventory.katana > 0 :
                inventory.katana -= 1
                char.katana = True
            else :
                pass
        elif r == "❌" :
            if inventory.shotgun > 0 :
                inventory.shotgun -= 1
                char.shotgun = True
            else :
                pass
        inventory.save()
        char.save()

    # allow the player to trade
    def trade(r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12) :
        goods = [int(r1),int(r2),int(r3),int(r4),int(r5),int(r6),int(r7),int(r8),int(r9),int(r10),int(r11),int(r12)]
        total = sum(goods)
        if total > 0 :
            return True
        else :
            return False

    # create enemies for fight   
    def enemygen(self,event):
        inventory = Inventory()
        inventory.loot()
        enemy = Player()
        enemy.pinv = inventory
        enemy.name = self.pk
        enemy.avatar = event.illus
        enemy.body = event.power
        enemy.mind = 2
        enemy.bonus1 = event.spe
        enemy.hp = event.power * 2
        enemy.maxhp = event.power * 2
        enemy.melee = event.power
        if event.name == "MECHA" or event.name == "BOUNTY HUNTERS" :
            enemy.dist = 3
        elif event.name == "MERCENARIES" or event.name == "BROKEN ROBOT" :
            enemy.dist = 2
        else :
            enemy.dist = 1
        enemy.aim = 2
        if event.power > 6 :
            enemy.speed = 2
        else :
            enemy.speed = 1
        if event.power > 8 :
            enemy.armor = 3
        elif event.power > 6 :
            enemy.armor = 2
        elif event.power > 4 :
            enemy.armor = 1
        else :
            enemy.armor = 0
        if event.name == "MECHA" or event.name == "BOUNTY HUNTERS" :
            enemy.range = 3
        elif event.name == "MERCENARIES" or event.name == "BROKEN ROBOT" :
            enemy.range = 2
        else :
            enemy.range = 1
        enemy.sick = False
        enemy.trauma = False
        enemy.tired = False
        enemy.wound = False
        if event.name == "MERCENARIES" or event.name == "RAIDERS" or event.name == "BOUNTY HUNTERS" or event.name == "EXOSKELETON" :
            enemy.katana = True
        else :
            enemy.katana = False
        if event.name == "MERCENARIES" or event.name == "BOUNTY HUNTERS" or event.name == "MECHA" :
            enemy.shotgun = True
        else :
            enemy.shotgun = False
        enemy.turn = False
        inventory.save()
        enemy.save()

    def heal(self,n):
        h = self.hp + n
        if h <= self.maxhp :
            self.hp += n
        else :
            pass

# Party - each player has it own party ( limited to 8 max )
class Party(models.Model):
    pplayer = models.OneToOneField(
        Player,
        on_delete=models.CASCADE,primary_key= True,
    )
    mem2 = models.IntegerField(default=0)
    mem3 = models.IntegerField(default=0)
    mem4 = models.IntegerField(default=0)
    mem5 = models.IntegerField(default=0)
    mem6 = models.IntegerField(default=0)
    mem7 = models.IntegerField(default=0)
    mem8 = models.IntegerField(default=0)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)

    # check if member exists in party or not
    def ismember(self,player,member):
        if member != 0 :
            mem = Player.objects.get(pk=member)
            return mem
        else :
            return player

    # count the number of members in the current party 
    def countmember(self):
        n = 1
        if self.mem2 != 0 :
            n += 1
        else :
            pass
        if self.mem3 != 0 :
            n += 1
        else :
            pass
        if self.mem4 != 0 :
            n += 1
        else :
            pass
        if self.mem5 != 0 :
            n += 1
        else :
            pass
        if self.mem6 != 0 :
            n += 1
        else :
            pass
        if self.mem7 != 0 :
            n += 1
        else :
            pass
        return n

    # return the list of all "player" objects in the party
    def partylist(self):
        pali = []
        if self.mem2 != 0 :
            pali.append(Player.objects.get(pk=self.mem2))
        else :
            pass
        if self.mem3 != 0 :
            pali.append(Player.objects.get(pk=self.mem3))
        else :
            pass
        if self.mem4 != 0 :
            pali.append(Player.objects.get(pk=self.mem4))
        else :
            pass
        if self.mem5 != 0 :
            pali.append(Player.objects.get(pk=self.mem5))
        else :
            pass
        if self.mem6 != 0 :
            pali.append(Player.objects.get(pk=self.mem6))
        else :
            pass
        if self.mem7 != 0 :
            pali.append(Player.objects.get(pk=self.mem7))
        else :
            pass
        return pali

    # check if there is a robot in the party
    def checkrobot(self,party,player):
        roblist = [
            party.ismember(player,party.mem2).name,
            party.ismember(player,party.mem3).name,
            party.ismember(player,party.mem4).name,
            party.ismember(player,party.mem5).name,
            party.ismember(player,party.mem6).name,
            party.ismember(player,party.mem7).name
        ]
        x = roblist.count("robot")
        return x

    # check all bonuses from party members
    def checkbonus(self,player,party,bonus):

        spelist = [
            player.bonus1,
            player.bonus2,
            party.ismember(player,party.mem2).bonus1,
            party.ismember(player,party.mem3).bonus1,
            party.ismember(player,party.mem4).bonus1,
            party.ismember(player,party.mem5).bonus1,
            party.ismember(player,party.mem6).bonus1,
            party.ismember(player,party.mem7).bonus1
            ]
        x = spelist.count(bonus)
        if x > 0 :
            return True
        else :
            return False
        
    # check all maluses from party members
    def checkmalus(self,player,party,malus):

        spelist = [
            player.malus1,
            player.malus2,
            party.ismember(player,party.mem2).malus1,
            party.ismember(player,party.mem3).malus1,
            party.ismember(player,party.mem4).malus1,
            party.ismember(player,party.mem5).malus1,
            party.ismember(player,party.mem6).malus1,
            party.ismember(player,party.mem7).malus1,
            ]
        x = spelist.count(malus)
        if x > 0 :
            return True
        else :
            return False
    
    # apply damage to all party members if threat is a group level
    def groupdmg(self,dmg):
        for x in self.partylist() :
            x.hp += dmg
            x.save()

    def select(self,char,player):
        char.selected = True
        group = self.partylist()
        for m in group :
            if m != char :
                m.selected = False
                m.save()
        if char != player :
            player.selected = False
            player.save()
        else :
            pass
        char.save()

    def selected(self,player):
        group = self.partylist()
        for m in group :
            if m.selected :
                return m
            else :
                continue
        if player.selected :
            return player
        else :
            return False

    def checkturn(self,player):
        part = self.partylist()
        for p in part :
            if p.turn :
                return True
            else :
                continue
        if player.turn :
            return True
        else :
            return False
        
# Event - events are encounters, findings, menaces happening randomly to the player or its shelters
class Event(models.Model):
    illus = models.ImageField(default='event.jpeg', blank=True)
    name = models.CharField()
    power = models.IntegerField(default=2,choices=Power.choices)
    spe = models.CharField(default="none")
    mal = models.CharField(default="none")
    type = models.CharField(default="none")
    crits = models.CharField(default="none")
    critst = models.CharField(default="none")
    succ = models.CharField(default="none")
    succt = models.CharField(default="none")
    fail = models.CharField(default="none")
    failt = models.CharField(default="none")
    critf = models.CharField(default="none")
    critft = models.CharField(default="none")
    group = models.BooleanField(default=False)
    sick = models.BooleanField(default=False)
    trauma = models.BooleanField(default=False)

    # generate all the events of the game
    def cards():
        a = 0
        while a < 53 :
            if a == 0 :
                event = Event()
                event.name = "JOKER"
                event.illus = 'joker.jpeg'
                event.power = 0
                event.spe = "none"
                event.mal = "none"
                event.type = "none"
                event.crits = "none"
                event.critst = "none"
                event.succ = "none"
                event.succt = "none"
                event.fail = "none"
                event.failt = "none"
                event.critf = "none"
                event.critft = "none"
                event.group = False
                event.sick = False
                event.trauma = False
                event.save()
                a += 1
            elif a == 1 :
                event = Event()
                event.name = "ROBOT"
                event.illus = 'robot.jpeg'
                event.power = 0
                event.spe = "Technician"
                event.mal = "Clumsy"
                event.type = "recrute"
                event.crits = "robot"
                event.critst = "recrute"
                event.succ = "robot"
                event.succt = "recrute"
                event.fail = "none"
                event.failt = "none"
                event.critf = "none"
                event.critft = "none"
                event.group = False
                event.sick = False
                event.trauma = False
                event.save()
                a += 1
            elif a == 2 :
                event = Event()
                event.name = "BOUNTY HUNTER"
                event.illus = "bounty.jpeg"
                event.power = 0
                event.spe = "Charming"
                event.mal = "Ugly"
                event.type = "recrute"
                event.crits = "bounty"
                event.critst = "recrute"
                event.succ = "bounty"
                event.succt = "recrute"
                event.fail = "none"
                event.failt = "none"
                event.critf = "none"
                event.critft = "none"
                event.group = False
                event.sick = False
                event.trauma = False
                event.save()
                a += 1
            elif a == 3 :
                event = Event()
                event.name = "MERCENARY"
                event.illus = "mercenary.jpeg"
                event.power = 0
                event.spe = "Charming"
                event.mal = "Ugly"
                event.type = "recrute"
                event.crits = "mercenary"
                event.critst = "recrute"
                event.succ = "mercenary"
                event.succt = "recrute"
                event.fail = "none"
                event.failt = "none"
                event.critf = "none"
                event.critft = "none"
                event.group = False
                event.sick = False
                event.trauma = False
                event.save()
                a += 1
            elif a == 4 :
                event = Event()
                event.name = "ENGENEER"
                event.illus = "engeneer.jpeg"
                event.power = 0
                event.spe = "Charming"
                event.mal = "Ugly"
                event.type = "recrute"
                event.crits = "engeneer"
                event.critst = "recrute"
                event.succ = "engeneer"
                event.succt = "recrute"
                event.fail = "none"
                event.failt = "none"
                event.critf = "none"
                event.critft = "none"
                event.group = False
                event.sick = False
                event.trauma = False
                event.save()
                a += 1
            elif a == 5 :
                event = Event()
                event.name = "DEALER"
                event.illus = "deal.jpeg"
                event.power = 0
                event.spe = "Charming"
                event.mal = "Ugly"
                event.type = "recrute"
                event.crits = "dealer"
                event.critst = "recrute"
                event.succ = "dealer"
                event.succt = "recrute"
                event.fail = "none"
                event.failt = "none"
                event.critf = "none"
                event.critft = "none"
                event.group = False
                event.sick = False
                event.trauma = False
                event.save()
                a += 1
            elif a == 6 :
                event = Event()
                event.name = "DOCTOR"
                event.illus = "doc.jpeg"
                event.power = 0
                event.spe = "Charming"
                event.mal = "Ugly"
                event.type = "recrute"
                event.crits = "doctor"
                event.critst = "recrute"
                event.succ = "doctor"
                event.succt = "recrute"
                event.fail = "none"
                event.failt = "none"
                event.critf = "none"
                event.critft = "none"
                event.group = False
                event.sick = False
                event.trauma = False
                event.save()
                a += 1
            elif a == 7 :
                event = Event()
                event.name = "MERCHANT"
                event.illus = "merch.jpeg"
                event.power = 0
                event.spe = "Charming"
                event.mal = "Ugly"
                event.type = "recrute"
                event.crits = "merchant"
                event.critst = "recrute"
                event.succ = "merchant"
                event.succt = "recrute"
                event.fail = "none"
                event.failt = "none"
                event.critf = "none"
                event.critft = "none"
                event.group = False
                event.sick = False
                event.trauma = False
                event.save()
                a += 1
            elif a == 8 :
                event = Event()
                event.name = "PETS"
                event.illus = "pets.jpeg"
                event.power = 0
                event.spe = "Biologist"
                event.mal = "Complotist"
                event.type = "recrute"
                event.crits = "queen"
                event.critst = "animals"
                event.succ = "horse"
                event.succt = "animals"
                event.fail = "dog"
                event.failt = "animals"
                event.critf = "cat"
                event.critft = "animals"
                event.group = False
                event.sick = False
                event.trauma = False
                event.save()
                a += 1
            elif a == 9 :
                event = Event()
                event.name = "COMMUNITY"
                event.illus = "community.jpeg"
                event.power = 0
                event.spe = "Charming"
                event.mal = "Ugly"
                event.type = "survivors"
                event.crits = "6"
                event.critst = "survivors"
                event.succ = "5"
                event.succt = "survivors"
                event.fail = "4"
                event.failt = "survivors"
                event.critf = "none"
                event.critft = "none"
                event.group = False
                event.sick = False
                event.trauma = False
                event.save()
                a += 1
            elif a == 10 :
                event = Event()
                event.name = "GROUP"
                event.illus = "group.jpeg"
                event.power = 0
                event.spe = "Charming"
                event.mal = "Ugly"
                event.type = "survivors"
                event.crits = "5"
                event.critst = "survivors"
                event.succ = "4"
                event.succt = "survivors"
                event.fail = "3"
                event.failt = "survivors"
                event.critf = "none"
                event.critft = "none"
                event.group = False
                event.sick = False
                event.trauma = False
                event.save()
                a += 1
            elif a == 11 :
                event = Event()
                event.name = "FAMILY"
                event.illus = "family.jpeg"
                event.power = 0
                event.spe = "Charming"
                event.mal = "Ugly"
                event.type = "survivors"
                event.crits = "4"
                event.critst = "survivors"
                event.succ = "3"
                event.succt = "survivors"
                event.fail = "2"
                event.failt = "survivors"
                event.critf = "none"
                event.critft = "none"
                event.group = False
                event.sick = False
                event.trauma = False
                event.save()
                a += 1
            elif a == 12 :
                event = Event()
                event.name = "COUPLE"
                event.illus = "couple.jpeg"
                event.power = 0
                event.spe = "Charming"
                event.mal = "Ugly"
                event.type = "survivors"
                event.crits = "3"
                event.critst = "survivors"
                event.succ = "2"
                event.succt = "survivors"
                event.fail = "1"
                event.failt = "survivors"
                event.critf = "none"
                event.critft = "none"
                event.group = False
                event.sick = False
                event.trauma = False
                event.save()
                a += 1
            elif a == 13 :
                event = Event()
                event.name = "WANDERER"
                event.illus = "wanderer.jpeg"
                event.power = 0
                event.spe = "Charming"
                event.mal = "Ugly"
                event.type = "survivors"
                event.crits = "2"
                event.critst = "survivors"
                event.succ = "1"
                event.succt = "survivors"
                event.fail = "0"
                event.failt = "survivors"
                event.critf = "none"
                event.critft = "none"
                event.group = False
                event.sick = False
                event.trauma = False
                event.save()
                a += 1
            elif a == 14 :
                event = Event()
                event.name = "WRECKAGE"
                event.illus = "wreckage.jpeg"
                event.power = 0
                event.spe = "Technician"
                event.mal = "Clumsy"
                event.type = "motors"
                event.crits = "tank"
                event.critst = "motors"
                event.succ = "van"
                event.succt = "motors"
                event.fail = "buggy"
                event.failt = "motors"
                event.critf = "moto"
                event.critft = "motors"
                event.group = False
                event.sick = False
                event.trauma = False
                event.save()
                a += 1
            elif a == 15 :
                event = Event()
                event.name = "IMPLANT"
                event.illus = "implant.jpeg"
                event.power = 0
                event.spe = "Biologist"
                event.mal = "Complotist"
                event.type = "finding"
                event.crits = "1"
                event.critst = "implant"
                event.succ = "1"
                event.succt = "implant"
                event.fail = "0"
                event.failt = "implant"
                event.critf = "none"
                event.critft = "none"
                event.group = False
                event.sick = False
                event.trauma = False
                event.save()
                a += 1
            elif a == 16 :
                event = Event()
                event.name = "?"
                event.illus = "unknown.jpeg"
                event.power = 0
                event.spe = "Biologist"
                event.mal = "Complotist"
                event.type = "finding"
                event.crits = "1"
                event.critst = "cure"
                event.succ = "1"
                event.succt = "cure"
                event.fail = "0"
                event.failt = "cure"
                event.critf = "none"
                event.critft = "none"
                event.group = False
                event.sick = False
                event.trauma = False
                event.save()
                a += 1
            elif a == 17 :
                event = Event()
                event.name = "BANDAGE"
                event.illus = "bandage.jpeg"
                event.power = 0
                event.spe = "Biologist"
                event.mal = "Complotist"
                event.type = "finding"
                event.crits = "3"
                event.critst = "bandage"
                event.succ = "2"
                event.succt = "bandage"
                event.fail = "1"
                event.failt = "bandage"
                event.critf = "none"
                event.critft = "none"
                event.group = False
                event.sick = False
                event.trauma = False
                event.save()
                a += 1
            elif a == 18 :
                event = Event()
                event.name = "TREASURE"
                event.illus = "treasure.jpeg"
                event.spe = "Focused"
                event.mal = "Careless"
                event.type = "finding"
                event.crits = "12"
                event.critst = "coins"
                event.succ = "8"
                event.succt = "coins"
                event.fail = "4"
                event.failt = "coins"
                event.critf = "1"
                event.critft = "coins"
                event.group = False
                event.sick = False
                event.trauma = False
                event.save()
                a += 1
            elif a == 19 :
                event = Event()
                event.power = 0
                event.name = "SUPPLIES"
                event.illus = "supplies.jpeg"
                event.spe = "Focused"
                event.mal = "Careless"
                event.type = "finding"
                event.crits = "6"
                event.critst = "fuel"
                event.succ = "6"
                event.succt = "metal"
                event.fail = "6"
                event.failt = "wood"
                event.critf = "6"
                event.critft = "food"
                event.group = False
                event.sick = False
                event.trauma = False
                event.save()
                a += 1
            elif a == 20 :
                event = Event()
                event.name = "RESTED"
                event.illus = "rested.jpeg"
                event.power = 0
                event.spe = ""
                event.mal = ""
                event.type = "finding"
                event.crits = "3"
                event.critst = "hp"
                event.succ = "2"
                event.succt = "hp"
                event.fail = "1"
                event.failt = "hp"
                event.critf = "0"
                event.critft = "hp"
                event.group = True
                event.sick = False
                event.trauma = False
                event.save()
                a += 1
            elif a == 21 :
                event = Event()
                event.name = "CURE"
                event.illus = "cure.jpeg"
                event.power = 0
                event.spe = "Biologist"
                event.mal = "Complotist"
                event.type = "finding"
                event.crits = "3"
                event.critst = "cure"
                event.succ = "2"
                event.succt = "cure"
                event.fail = "1"
                event.failt = "cure"
                event.critf = "0"
                event.critft = "cure"
                event.group = False
                event.sick = False
                event.trauma = False
                event.save()
                a += 1
            elif a == 22 :
                event = Event()
                event.name = "HIDEOUT"
                event.illus = "hideout.jpeg"
                event.power = 0
                event.spe = "Focused"
                event.mal = "Careless"
                event.type = "finding"
                event.crits = "6"
                event.critst = "coins"
                event.succ = "4"
                event.succt = "coins"
                event.fail = "2"
                event.failt = "coins"
                event.critf = "0"
                event.critft = "coins"
                event.group = False
                event.sick = False
                event.trauma = False
                event.save()
                a += 1
            elif a == 23 :
                event = Event()
                event.name = "PLAN'S PART"
                event.illus = "plan.jpeg"
                event.power = 0
                event.spe = "Focused"
                event.mal = "Careless"
                event.type = "finding"
                event.crits = "3"
                event.critst = "pp"
                event.succ = "2"
                event.succt = "pp"
                event.fail = "1"
                event.failt = "pp"
                event.critf = "0"
                event.critft = "pp"
                event.group = False
                event.sick = False
                event.trauma = False
                event.save()
                a += 1
            elif a == 24 :
                event = Event()
                event.name = "SHORTCUT"
                event.illus = "shortcut.jpeg"
                event.power = 0
                event.spe = "Focused"
                event.mal = "Careless"
                event.type = "finding"
                event.crits = "6"
                event.critst = "fuel"
                event.succ = "6"
                event.succt = "food"
                event.fail = "3"
                event.failt = "food"
                event.critf = "1"
                event.critft = "food"
                event.group = False
                event.sick = False
                event.trauma = False
                event.save()
                a += 1
            elif a == 25 :
                event = Event()
                event.name = "DOPAGE"
                event.illus = "dopage.jpeg"
                event.power = 0
                event.spe = "Biologist"
                event.mal = "Complotist"
                event.type = "finding"
                event.crits = "3"
                event.critst = "drug"
                event.succ = "2"
                event.succt = "drug"
                event.fail = "1"
                event.failt = "drug"
                event.critf = "0"
                event.critft = "drug"
                event.group = False
                event.sick = False
                event.trauma = False
                event.save()
                a += 1
            elif a == 26 :
                event = Event()
                event.name = "FOOD"
                event.illus = "food.jpeg"
                event.power = 0
                event.spe = "Focused"
                event.mal = "Careless"
                event.type = "finding"
                event.crits = "6"
                event.critst = "food"
                event.succ = "4"
                event.succt = "food"
                event.fail = "2"
                event.failt = "food"
                event.critf = "1"
                event.critft = "food"
                event.group = False
                event.sick = False
                event.trauma = False
                event.save()
                a += 1
            elif a == 27 :
                event = Event()
                event.name = "GIANT MUTATION"
                event.illus = "giant.jpeg"
                event.power = 10
                event.spe = "Powerful"
                event.mal = "Weak"
                event.type = "monster"
                event.crits = "12"
                event.critst = "coins"
                event.succ = "24"
                event.succt = "food"
                event.fail = "-2"
                event.failt = "hp"
                event.critf = "-3"
                event.critft = "hp"
                event.group = True
                event.sick = False
                event.trauma = True
                event.save()
                a += 1
            elif a == 28 :
                event = Event()
                event.name = "WAR MECHA"
                event.illus = "mecha.jpeg"
                event.power = 10
                event.spe = "Powerful"
                event.mal = "Weak"
                event.type = "monster"
                event.crits = "12"
                event.critst = "coins"
                event.succ = "12"
                event.succt = "metal"
                event.fail = "-1"
                event.failt = "hp"
                event.critf = "-2"
                event.critft = "hp"
                event.group = True
                event.sick = False
                event.trauma = True
                event.save()
                a += 1
            elif a == 29 :
                event = Event()
                event.name = "QUEEN"
                event.illus = "queen.jpeg"
                event.power = 8
                event.spe = "Powerful"
                event.mal = "Weak"
                event.type = "monster"
                event.crits = "6"
                event.critst = "coins"
                event.succ = "6"
                event.succt = "food"
                event.fail = "-3"
                event.failt = "hp"
                event.critf = "-1"
                event.critft = "hp"
                event.group = True
                event.sick = False
                event.trauma = True
                event.save()
                a += 1
            elif a == 30 :
                event = Event()
                event.name = "PACK OF ALPHAS"
                event.illus = "alphas.jpeg"
                event.power = 8
                event.spe = "Athletic"
                event.mal = "Asthmatic"
                event.type = "monster"
                event.crits = "6"
                event.critst = "food"
                event.succ = "dog"
                event.succt = "animals"
                event.fail = "-2"
                event.failt = "hp"
                event.critf = "-1"
                event.critft = "hp"
                event.group = True
                event.sick = False
                event.trauma = True
                event.save()
                a += 1
            elif a == 31 :
                event = Event()
                event.name = "BOUNTY HUNTERS"
                event.illus = "hunters.jpeg"
                event.power = 6
                event.spe = "Discrete"
                event.mal = "Loud"
                event.type = "menace"
                event.crits = "1"
                event.critst = "shotgun"
                event.succ = "6"
                event.succt = "coins"
                event.fail = "-2"
                event.failt = "hp"
                event.critf = "-3"
                event.critft = "hp"
                event.group = False
                event.sick = False
                event.trauma = False
                event.save()
                a += 1
            elif a == 32 :
                event = Event()
                event.name = "MERCENARIES"
                event.illus = "mercos.jpeg"
                event.power = 6
                event.spe = "Athletic"
                event.mal = "Asthmatic"
                event.type = "menace"
                event.crits = "1"
                event.critst = "katana"
                event.succ = "6"
                event.succt = "coins"
                event.fail = "-2"
                event.failt = "hp"
                event.critf = "-3"
                event.critft = "hp"
                event.group = False
                event.sick = False
                event.trauma = False
                event.save()
                a += 1
            elif a == 33 :
                event = Event()
                event.name = "ACCIDENT"
                event.illus = "accident.jpeg"
                event.power = 6
                event.spe = "Focused"
                event.mal = "Careless"
                event.type = "natural"
                event.crits = "engeneer"
                event.critst = "recrute"
                event.succ = "3"
                event.succt = "fuel"
                event.fail = "-1"
                event.failt = "hp"
                event.critf = "-1"
                event.critft = "hp"
                event.group = True
                event.sick = False
                event.trauma = False
                event.save()
                a += 1
            elif a == 34 :
                event = Event()
                event.name = "MUTANTS"
                event.illus = "mutants.jpeg"
                event.power = 4
                event.spe = "Athletic"
                event.mal = "Asthmatic"
                event.type = "menace"
                event.crits = "3"
                event.critst = "coins"
                event.succ = "2"
                event.succt = "survivors"
                event.fail = "-2"
                event.failt = "hp"
                event.critf = "-1"
                event.critft = "hp"
                event.group = True
                event.sick = False
                event.trauma = True
                event.save()
                a += 1
            elif a == 35 :
                event = Event()
                event.name = "RAIDERS"
                event.illus = "raiders.jpeg"
                event.power = 4
                event.spe = "Athletic"
                event.mal = "Asthmatic"
                event.type = "menace"
                event.crits = "3"
                event.critst = "fuel"
                event.succ = "3"
                event.succt = "coins"
                event.fail = "-3"
                event.failt = "coins"
                event.critf = "-1"
                event.critft = "hp"
                event.group = True
                event.sick = False
                event.trauma = True
                event.save()
                a += 1
            elif a == 36 :
                event = Event()
                event.name = "PREDATORS"
                event.illus = "predators.jpeg"
                event.power = 4
                event.spe = "Athletic"
                event.mal = "Asthmatic"
                event.type = "menace"
                event.crits = "dog"
                event.critst = "animals"
                event.succ = "3"
                event.succt = "food"
                event.fail = "-1"
                event.failt = "hp"
                event.critf = "-2"
                event.critft = "hp"
                event.group = False
                event.sick = False
                event.trauma = True
                event.save()
                a += 1
            elif a == 37 :
                event = Event()
                event.name = "ZOMBIS"
                event.illus = "zombis.jpeg"
                event.power = 2
                event.spe = "Discrete"
                event.mal = "Loud"
                event.type = "monster"
                event.crits = "1"
                event.critst = "survivors"
                event.succ = "2"
                event.succt = "coins"
                event.fail = "-1"
                event.failt = "hp"
                event.critf = "-2"
                event.critft = "hp"
                event.group = False
                event.sick = True
                event.trauma = True
                event.save()
                a += 1
            elif a == 38 :
                event = Event()
                event.name = "BANDITS"
                event.illus = "bandits.jpeg"
                event.power = 2
                event.spe = "Discrete"
                event.mal = "Loud"
                event.type = "menace"
                event.crits = "3"
                event.critst = "coins"
                event.succ = "2"
                event.succt = "coins"
                event.fail = "-2"
                event.failt = "coins"
                event.critf = "-3"
                event.critft = "coins"
                event.group = False
                event.sick = False
                event.trauma = False
                event.save()
                a += 1
            elif a == 39 :
                event = Event()
                event.name = "INJURY"
                event.illus = "injury.jpeg"
                event.power = 2
                event.spe = "Focused"
                event.mal = "Careless"
                event.type = "science"
                event.crits = "doctor"
                event.critst = "recrute"
                event.succ = "1"
                event.succt = "bandage"
                event.fail = "-1"
                event.failt = "hp"
                event.critf = "-2"
                event.critft = "hp"
                event.group = False
                event.sick = False
                event.trauma = False
                event.save()
                a += 1
            elif a == 40 :
                event = Event()
                event.name = "IEM WEAPON"
                event.illus = "iem.jpeg"
                event.power = 10
                event.spe = "Technician"
                event.mal = "Clumsy"
                event.type = "science"
                event.crits = "tank"
                event.critst = "motors"
                event.succ = "12"
                event.succt = "fuel"
                event.fail = "none"
                event.failt = "none"
                event.critf = "-1"
                event.critft = "hp"
                event.group = True
                event.sick = False
                event.trauma = False
                event.save()
                a += 1
            elif a == 41 :
                event = Event()
                event.name = "EXOSKELETON"
                event.illus = "exo.jpeg"
                event.power = 10
                event.spe = "Technician"
                event.mal = "Clumsy"
                event.type = "menace"
                event.crits = "1"
                event.critst = "armors"
                event.succ = "12"
                event.succt = "metal"
                event.fail = "-1"
                event.failt = "hp"
                event.critf = "-2"
                event.critft = "hp"
                event.group = True
                event.sick = False
                event.trauma = False
                event.save()
                a += 1
            elif a == 42 :
                event = Event()
                event.name = "BROKEN ROBOT"
                event.illus = "broken.jpeg"
                event.power = 8
                event.spe = "Technician"
                event.mal = "Clumsy"
                event.type = "monster"
                event.crits = "robot"
                event.critst = "recrute"
                event.succ = "6"
                event.succt = "metal"
                event.fail = "-2"
                event.failt = "hp"
                event.critf = "-3"
                event.critft = "hp"
                event.group = False
                event.sick = False
                event.trauma = True
                event.save()
                a += 1
            elif a == 43 :
                event = Event()
                event.name = "HACKING"
                event.illus = "hack.jpeg"
                event.power = 8
                event.spe = "Technician"
                event.mal = "Clumsy"
                event.type = "science"
                event.crits = "6"
                event.critst = "coins"
                event.succ = "3"
                event.succt = "coins"
                event.fail = "-1"
                event.failt = "coins"
                event.critf = "-2"
                event.critft = "coins"
                event.group = True
                event.sick = False
                event.trauma = False
                event.save()
                a += 1
            elif a == 44 :
                event = Event()
                event.name = "RADIATIONS"
                event.illus = "rads.jpeg"
                event.power = 6
                event.spe = "Biologist"
                event.mal = "Complotist"
                event.type = "science"
                event.crits = "6"
                event.critst = "fuel"
                event.succ = "3"
                event.succt = "fuel"
                event.fail = "-2"
                event.failt = "hp"
                event.critf = "-1"
                event.critft = "hp"
                event.group = False
                event.sick = True
                event.trauma = False
                event.save()
                a += 1
            elif a == 45 :
                event = Event()
                event.name = "EPIDEMY"
                event.illus = "epidemy.jpeg"
                event.power = 6
                event.spe = "Biologist"
                event.mal = "Complotist"
                event.type = "science"
                event.crits = "3"
                event.critst = "survivors"
                event.succ = "1"
                event.succt = "cure"
                event.fail = "-3"
                event.failt = "survivors"
                event.critf = "-5"
                event.critft = "survivors"
                event.group = True
                event.sick = True
                event.trauma = False
                event.save()
                a += 1
            elif a == 46 :
                event = Event()
                event.name = "PARASITE"
                event.illus = "parasite.jpeg"
                event.power = 6
                event.spe = "Biologist"
                event.mal = "Complotist"
                event.type = "science"
                event.crits = "1"
                event.critst = "cure"
                event.succ = "3"
                event.succt = "food"
                event.fail = "-3"
                event.failt = "food"
                event.critf = "-5"
                event.critft = "food"
                event.group = False
                event.sick = True
                event.trauma = False
                event.save()
                a += 1
            elif a == 47 :
                event = Event()
                event.name = "BROTHEL"
                event.illus = "broth.jpeg"
                event.power = 4
                event.spe = "Focused"
                event.mal = "Careless"
                event.type = "charisma"
                event.crits = "2"
                event.critst = "hp"
                event.succ = "1"
                event.succt = "hp"
                event.fail = "-1"
                event.failt = "coins"
                event.critf = "-2"
                event.critft = "coins"
                event.group = True
                event.sick = True
                event.trauma = False
                event.save()
                a += 1
            elif a == 48 :
                event = Event()
                event.name = "HEAVY FOG"
                event.illus = "fog.jpeg"
                event.power = 4
                event.spe = "Focused"
                event.mal = "Careless"
                event.type = "natural"
                event.crits = "2"
                event.critst = "survivors"
                event.succ = "1"
                event.succt = "survivors"
                event.fail = "-1"
                event.failt = "survivors"
                event.critf = "-2"
                event.critft = "survivors"
                event.group = False
                event.sick = False
                event.trauma = False
                event.save()
                a += 1
            elif a == 49 :
                event = Event()
                event.name = "TRAP"
                event.illus = "trap.jpeg"
                event.power = 4
                event.spe = "Focused"
                event.mal = "Careless"
                event.type = "charisma"
                event.crits = "3"
                event.critst = "metal"
                event.succ = "3"
                event.succt = "wood"
                event.fail = "-1"
                event.failt = "hp"
                event.critf = "-2"
                event.critft = "hp"
                event.group = False
                event.sick = False
                event.trauma = False
                event.save()
                a += 1
            elif a == 50 :
                event = Event()
                event.name = "SLAVERS"
                event.illus = "slavers.jpeg"
                event.power = 2
                event.spe = "Charming"
                event.mal = "Ugly"
                event.type = "menace"
                event.crits = "3"
                event.critst = "survivors"
                event.succ = "2"
                event.succt = "survivors"
                event.fail = "-2"
                event.failt = "survivors"
                event.critf = "-3"
                event.critft = "survivors"
                event.group = False
                event.sick = False
                event.trauma = True
                event.save()
                a += 1
            elif a == 51 :
                event = Event()
                event.name = "PUBLIC DEBATE"
                event.illus = "debate.jpeg"
                event.power = 2
                event.spe = "Charming"
                event.mal = "Ugly"
                event.type = "charisma"
                event.crits = "2"
                event.critst = "survivors"
                event.succ = "1"
                event.succt = "survivors"
                event.fail = "3"
                event.failt = "food"
                event.critf = "-2"
                event.critft = "survivors"
                event.group = False
                event.sick = False
                event.trauma = False
                event.save()
                a += 1
            else :
                event = Event()
                event.name = "ANGRY MOB"
                event.illus = "mob.jpeg"
                event.power = 2
                event.spe = "Charming"
                event.mal = "Ugly"
                event.type = "menace"
                event.crits = "3"
                event.critst = "wood"
                event.succ = "2"
                event.succt = "coins"
                event.fail = "-1"
                event.failt = "coins"
                event.critf = "-2"
                event.critft = "coins"
                event.group = True
                event.sick = False
                event.trauma = False
                event.save()
                a += 1

    # add or remove resources or items from the player's inventory
    def resource(self, inventory, res, qtt):

        amount = int(qtt)

        if res == "food" :
            inventory.food += amount
        elif res == "wood" :
            inventory.wood += amount
        elif res == "metal" :
            inventory.metal += amount
        elif res == "fuel" :
            inventory.fuel += amount
        elif res == "bandage" :
            inventory.bandage += amount
        elif res == "med" :
            inventory.med += amount
        elif res == "drug" :
            inventory.drug += amount
        elif res == "armor":
            inventory.armor += amount
        elif res == "implant":
            inventory.implant += amount
        elif res == "katana":
            inventory.katana += amount
        elif res == "shotgun":
            inventory.shotgun += amount
        elif res == "coins":
            inventory.coins += amount
        elif res == "pp":
            inventory.pp += amount
        else :
            inventory.cure += amount
        inventory.save()

    
    def resolution(self,player,party,inventory,reso):
            
            if reso == "critss" :
                res = self.critst
                t = self.crits
            elif reso == "success" :
                res = self.succt
                t = self.succ
            elif reso == "fail" :
                res = self.failt
                t = self.fail
            else :
                res = self.critft
                t = self.critf

            if res == "none" :
                pass
            elif res == "hp" :
                if self.group == True :
                    party.groupdmg(int(t))
                    player.hp += int(t)
                else :
                    player.hp += int(t)
            elif res != "survivors" and res != "motors" and res != "animals" and res != "recrute":
                self.resource(inventory, res, t)
            elif self.critst == "survivors" :
                player.surv += int(t)
            else :
                if self.type == "recrute" and self.pk > 4 :
                    if Region.checkfounder(player) :
                        player.recrute(t,party)
                    else :
                        player.journal = "you "
                        pass
                elif self.critst == "motors":
                    player.move = "motor"
                else :
                    player.recrute(t,party)
            if reso != "fail" and reso != "oups" :
                verb = "you found"
            else :
                verb = "you lost"
            info = verb + " " + self.crits + " " + self.critst
            player.journal = info
            inventory.save()
            player.save()
            party.save()

# Fight field - the place where the fight happens !

class FightField(models.Model):
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    name = models.CharField(default="")
    char = models.IntegerField(default=0)
    icon = models.ImageField(default='member.jpeg', blank=True)

    def versus(player):    
        a = 1
        b = 1
        while a < 11 and b < 11:
            ff = FightField()
            ff.name = player.name
            ff.x = a
            ff.y = b
            ff.save()
            a += 1
            if a == 11:
                b += 1
                a = 1
            else :
                continue

    def placenemies(enemies):
        print(enemies)
        if len(enemies) == 1 :
            z = FightField.objects.get(x=5,y=1)
            z.char = enemies[0].pk
            z.save()
        elif len(enemies) == 2 :
            z1 = FightField.objects.get(x=6,y=1)
            z2 = FightField.objects.get(x=4,y=1)
            z1.char = enemies[0].pk
            z2.char = enemies[1].pk
            z1.save()
            z2.save()
        else :
            z1 = FightField.objects.get(x=7,y=1)
            z2 = FightField.objects.get(x=5,y=1)
            z3 = FightField.objects.get(x=3,y=1)
            z1.char = enemies[0].pk
            z2.char = enemies[1].pk
            z3.char = enemies[2].pk
            z1.save()
            z2.save()
            z3.save()

    def checkdist(self,new,n):
        a = self.x - new.x
        b = self.y - new.y
        print(n)
        print(a," = ",self.x," - ",new.x)
        print(b," = ",self.y," - ",new.y)
        if a <= n or a >= -n and b <= n or b >= -n :
            print("you can place here")
            return True
        else :
            print("you can't place here")
            return False

    def place(self,char):
        if char.start :
            if self.char == 0 :
                self.char = char.pk
                char.start = False
                char.save()
                self.save()
            else :
                print("already someone here")
                pass
        elif char.turn :
            previous = FightField.objects.get(char=char.pk)
            print(previous.pk,self.char,char.turn)
            self.char = char.pk
            previous.char = 0
            char.turn = False
            previous.save()
            self.save()
            char.save()
            print(previous.pk,self.char,char.turn)
        else :
            print("wtf ?")
            pass
        
    def checkab(self,a,b):
        if a > 0 and b > 0 and a < 10 and b < 10 :
            return True
        else :
            return False
        
    def lookaround(self,enemies):
        x = self.x
        y = self.y
        n = 5   
        a = x + n
        b = y + n
        c = x - n
        d = y - n
        while a >= c and b >= d:
            print(" self : ",self)
            print(" self x : ",x)
            print(" self y : ",y)
            print(" distance n : ",n)
            print(" x + n : ",a)
            print(" y + n : ",b)
            print(" x - n : ",c)
            print(" y - n : ",d)
                
            if self.checkab(a,b) :
                ff = FightField.objects.get(x=a,y=b)
                if ff.char != 0 :
                    target = Player.objects.get(pk=ff.char)
                    if target not in enemies :
                        print("target found",target.name,ff.x,ff.y,n)
                        datas = ff
                        return datas
                    else :
                        if a == c :
                            a = x + n
                            b -= 1
                            if self.checkab(a,b) :       
                                ff = FightField.objects.get(x=a,y=b)
                                if ff.char != 0 :
                                    target = Player.objects.get(pk=ff.char)
                                    if target not in enemies :
                                        print("target found",target.name,ff.x,ff.y,n)
                                        datas = ff
                                        return datas
                                    else :
                                        continue
                                else :
                                    continue
                            else :
                                a-=1
                                continue
                        else :
                            a-=1
                            continue
                else :
                    if a == c :
                            a = x + n
                            b -= 1
                            if self.checkab(a,b) :       
                                ff = FightField.objects.get(x=a,y=b)
                                if ff.char != 0 :
                                    target = Player.objects.get(pk=ff.char)
                                    if target not in enemies :
                                        print("target found",target.name,ff.x,ff.y,n)
                                        datas = ff
                                        return datas
                                    else :
                                        continue
                                else :
                                    continue
                            else :
                                a-=1
                                continue
                    else :
                        a-=1
                        continue
            else : 
                print("checkab failed")            
                if a == c :
                            a = x + n
                            b -= 1
                            if self.checkab(a,b) :       
                                ff = FightField.objects.get(x=a,y=b)
                                if ff.char != 0 :
                                    target = Player.objects.get(pk=ff.char)
                                    if target not in enemies :
                                        print("target found",target.name,ff.x,ff.y)
                                        datas = ff
                                        return datas
                                    else :
                                        continue
                                else :
                                    continue
                            else :
                                a-=1
                                continue
                else :
                    a-=1
                    continue
        datas = self
        print("no target found", datas.pk)
        return datas

    def move(self, n) :
        x = self.x + random.randint(-n,+n)
        y = self.y + random.randint(-n,+n)
        print(self.x,self.y,x,y)
        if self.checkab(x,y):
            if FightField.objects.get(x=x,y=y).char == 0 :
                print(x,y)
                nfield = FightField.objects.get(x=x,y=y)
                nfield.char = self.char
                nfield.save()
                print("I moved to",x,y)
                return True
            else :
                print("can't move to",x,y,FightField.objects.get(x=x,y=y).char)
                self.move(n)
        else :
            pass

    def goto(self,enemies):

        enemy = Player.objects.get(pk=self.char)
        if enemy.turn :
            print("enemy : ",enemy.pk)

            # check if a target is in range :

            datas = self.lookaround(enemies)
            target = Player.objects.get(pk=datas.char)
            print("datas : ",datas.char)
            if datas.char != self.char and datas.char != 0 and target not in enemies:
                charound = target
            else :
                charound = enemy

            # if target in range and target not ally :
            print(datas,enemy.range,charound,list(enemies))
            if self.checkdist(datas,enemy.range) and charound not in list(enemies) :
                print(" range attack ")
                self.attack(datas,enemy.range)
            elif self.checkdist(datas,enemy.melee) and charound not in list(enemies) :
                print(" melee attack ")
                self.attack(datas,enemy.melee)

            # else move !
            else :

                # if no target in range, move random !
                if datas == self :
                    if enemy.speed == 1 :
                        if datas.move(1) :
                            self.char = 0
                        else :
                            pass
                    elif enemy.speed == 2 :
                        if datas.move(2) :
                            self.char = 0
                        else :
                            pass
                    self.save()
                else :
                    if enemy.speed == 1 :
                        print("c'est pas moi, je bouge")
                        xmove = datas.x - self.x
                        ymove = datas.y - self.y
                        print(datas.x,datas.y)
                        print(self.x,self.y)
                        print(xmove,ymove)
                        if xmove > 0 :
                            nx = self.x + 1
                        else :
                            nx = self.x - 1
                        if ymove > 0 :
                            ny = self.y + 1
                        else :
                            ny = self.y - 1
                    else :
                        xmove = datas.x - self.x
                        ymove = datas.y - self.y
                        if xmove > 0 :
                            nx = self.x + 2
                        else :
                            nx = self.x - 2
                        if ymove > 0 :
                            ny = self.x + 2
                        else :
                            ny = self.x - 2
                        if datas.x == nx :
                            if xmove > 0 :
                                nx -= 1
                            else :
                                nx += 1
                        else :
                            pass
                        if datas.y == ny :
                            if ymove > 0 :
                                ny -= 1
                            else :
                                ny += 1
                        else :
                            pass
                    nfield = FightField.objects.get(x=nx,y=ny)
                    if self.char == nfield.char :
                        pass
                    else :
                        nfield.char = self.char
                        self.char = 0
                        self.save()
                        nfield.save()
                        datas.save()
            enemy.turn = False
            enemy.save()
            victim = Player.objects.get(pk=datas.char)
            print(victim.hp, " end of goto ",victim.name)
        else :
            print("je passe par là ?")
            pass

    def aiming(self,n):
        aim = random.randint(1,100)
        if n == 1 and aim < 50 :
            return True
        elif n == 2 and aim < 70 :
            return True
        elif n == 3 :
            return True
        else :
            return False
            
    def attack(self,vic,n):
        attacker = Player.objects.get(pk=self.char)
        victim = Player.objects.get(pk=vic.char)
        melee = attacker.melee - victim.armor
        range = attacker.range - victim.armor

        if n > 1 :
            if self.aiming(attacker.aim):
                print(" aiming ",victim.name," for ",range)
                victim.hp -= range
                print(victim.hp)
                victim.save()
            else :
                print(" missed ! ")
                pass
        else :
            print(" hitting ", victim.name,"for",melee)
            victim.hp -= melee
            print(victim.hp)
            victim.save()
            print(victim.name, victim.hp)

    def end(player,enem) :
        print("checking for end of fight")
        l = FightField.objects.all().filter(name=player.name)
        if player.hp <= 0 :
            return True
        else :
            print("player is still alive !")
            pass
        for ff in l :
            if ff.char not in enem :
                continue
            else :
                return False
        l.delete()
        return True