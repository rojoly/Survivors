from django.shortcuts import render, redirect, HttpResponse
from . import views
from .models import Inventory, Region, Player, Event, Party, FightField
from django.contrib.auth.decorators import login_required
from . import forms
from .forms import Trade, Item
import random, json
from PIL import Image

# Lists used to give datas to iterated objects during the game
Civ = ["Camp","Shelter","Fortress"]
Nature = ["Aquatic","Desert","Forest","Mountain","Plain"]
Colors = ["rgb(19, 35, 128)","rgb(222, 217, 175)","rgb(103, 128, 96)","rgb(241, 242, 240)","rgb(209, 224, 168)"]

# PLAYER VIEW ( WITH HUD ) - game's main view
@login_required(login_url="/users/login")
def game(request):

    # GENERATE DATAS

    
    player = Player.objects.get(name=request.user.username)
    if player.hp < 1 :
        return redirect("game:rip")
    else :
        pass
    region = Region.objects.get(x=player.x,y=player.y)
    playerinv = Inventory.objects.get(id=player.pinv_id)
    regioninv = Inventory.objects.get(id=region.rinv_id)
    party = Party.objects.get(pplayer=player.pk)
    group = []
    if party.ismember(player,party.mem2) != player :
        mem2 = Player.objects.get(pk=party.mem2)
        group.append(mem2)
    else :
        pass
    if party.ismember(player,party.mem3) != player :
        mem3 = Player.objects.get(pk=party.mem3)
        group.append(mem3)
    else :
        pass
    if party.ismember(player,party.mem4) != player :
        mem4 = Player.objects.get(pk=party.mem4)
        group.append(mem4)
    else :
        pass
    if party.ismember(player,party.mem5) != player :
        mem5 = Player.objects.get(pk=party.mem5)
        group.append(mem5)
    else :
        pass
    if party.ismember(player,party.mem6) != player :
        mem6 = Player.objects.get(pk=party.mem6)
        group.append(mem6)
    else :
        pass
    if party.ismember(player,party.mem7) != player :
        mem7 = Player.objects.get(pk=party.mem7)
        group.append(mem7)
    else :
        pass
    if party.ismember(player,party.mem8) != player :
        mem8 = Player.objects.get(pk=party.mem8)
        group.append(mem8)
    else :
        pass
    
    # CHECK IF PLAYER IS OCCUPIED

    if player.occupied != "free" and player.occupied != "fight" :
        return redirect("game:event")
    elif player.occupied == "fight" :
        return redirect("game:fight")
    else :
        pass

    # IF PLAYER SEND DATAS

    if request.method == "POST":

        x = 0
        check = True
        trade = Trade(request.POST)

        if trade.is_valid():
            Res = [
                    request.POST['food'],
                    request.POST['wood'],
                    request.POST['metal'],
                    request.POST['fuel'],
                    request.POST['bandage'],
                    request.POST['med'],
                    request.POST['drug'],
                    request.POST['cure'],
                    request.POST['katana'],
                    request.POST['shotgun'],
                    request.POST['armor'],
                    request.POST['implant']
                ]

            while x < 9 :
                if x == 0 :
                    playerinv.food += int(Res[x])              
                    if playerinv.food >= 0 :
                        regioninv.food -= int(Res[x])
                    else :
                        check = False
                    x +=1
                elif x == 1 :
                    playerinv.wood += int(Res[x])
                    if playerinv.wood >= 0 :
                        regioninv.wood -= int(Res[x])
                    else :
                        check = False
                    x +=1
                elif x == 2 :
                    playerinv.metal += int(Res[x])
                    if playerinv.metal >= 0 :
                        regioninv.metal -= int(Res[x])
                    else :
                        check = False
                    x +=1
                elif x == 3 :
                    playerinv.fuel += int(Res[x])
                    if playerinv.fuel >= 0 :
                        regioninv.fuel -= int(Res[x])
                    else :
                        check = False
                    x +=1
                elif x == 4 :
                    playerinv.med += int(Res[x])
                    if playerinv.med >= 0 :
                        regioninv.med -= int(Res[x])
                    else :
                        check = False
                    x +=1
                elif x == 5 :
                    playerinv.drug += int(Res[x])
                    if playerinv.drug >= 0 :
                        regioninv.drug -= int(Res[x])
                    else :
                        check = False
                    x +=1
                elif x == 6 :
                    playerinv.katana += int(Res[x])
                    if playerinv.katana >= 0 :
                        regioninv.katana -= int(Res[x])
                    else :
                        check = False
                    x +=1
                elif x == 7 :
                    playerinv.shotgun += int(Res[x])
                    if playerinv.shotgun >= 0 :
                        regioninv.shotgun -= int(Res[x])
                    else :
                        check = False
                    x +=1
                else :
                    playerinv.armor += int(Res[x])
                    if playerinv.armor >= 0 :
                        regioninv.armor -= int(Res[x])
                    else :
                        check = False
                    x +=1

            Merchant = [int(Res[0])*1,int(Res[1])*2,int(Res[2])*5,int(Res[3])*10]
            Medecine = [int(Res[4])*5,int(Res[5])*10,int(Res[6])*20,int(Res[7])*100]
            Dealer = [int(Res[8])*200,int(Res[9])*500]
            Mecano = [int(Res[10])*100,int(Res[11]*1000)]

            total = sum(Merchant) + sum(Medecine) + sum(Dealer) + sum(Mecano)
            max = regioninv.coins + total

            if total >= 0 and total <= playerinv.coins :
                playerinv.coins -= total
                regioninv.coins += total
                playerinv.save()
                regioninv.save()
                player.journal = "you traded at a market place."
                player.save()
                return redirect("game:ingame")
            elif total <=0 and max >= 0 and check :
                playerinv.coins -= total
                regioninv.coins += total
                playerinv.save()
                regioninv.save()
                player.journal = "you traded at a market place."
                player.save()
                return redirect("game:ingame")
            elif check :
                player.journal = "not enough coins to make the deal."
                player.save()
                return redirect("game:ingame")
            else :
                player.journal = "you can't sell what you don't have !"
                player.save()
                return redirect("game:ingame")
        else :
            print("else...")
            if request.POST.__contains__("wound"):
                Player.use(player,playerinv,party,request.POST['wound'])
            elif request.POST.__contains__("sick"):
                Player.use(player,playerinv,party,request.POST['sick'])
            elif request.POST.__contains__("trauma"):
                Player.use(player,playerinv,party,request.POST['trauma'])
            elif request.POST.__contains__("equiparm"):
                Player.use(player,playerinv,party,request.POST['equiparm'])
            elif request.POST.__contains__("equipkat"):
                Player.use(player,playerinv,party,request.POST['equipkat'])
            elif request.POST.__contains__("equipshot") :
                Player.use(player,playerinv,party,request.POST['equipshot'])
            else :
                pass
            return redirect("game:ingame")
        
    else:
        n = len(group)
        return render(
            request, 
            'game/hud.html', 
            context={ 
                'player': player,
                'region' : region,
                'playerinv' : playerinv,
                'regioninv' : regioninv,
                'party' : party,
                'group' : group,
                'n' : n
                  })

# WORLD MAP VIEW - open in a new window
@login_required(login_url="/users/login")
def map(request):

    player = Player.objects.get(name=request.user.username)
    party = Party.objects.get(pplayer=player.pk)
    inventory = Inventory.objects.get(id=player.pinv_id)
    region = Region.objects.get(x=player.x,y=player.y)
    world = Region.objects.all()
    shelters = []
    for r in world :
        if r.founder == player.name :
            shelters.append(r)
        else :
            pass

    # check if player is not already in an event or a fight...

    if player.occupied == "inevent" :
        return redirect("game:event")
    elif player.occupied == "infight" :
        return redirect("game:fight")
    else :
        pass

    # if form is sent...

    if request.method == "POST":

        olx = player.x
        oly = player.y
        player.x = request.POST['x']
        player.y = request.POST['y']
        newregion = Region.objects.get(x=player.x,y=player.y)
        player.save()

        # check if player have the requirements...

        if player.travel(player,party,inventory,olx,oly,newregion.x,newregion.y) :

            if newregion.discovered :
                if player.countdown == 1 :                   
                    newregion.save()
                    player.countdown += 1
                    player.distance += 1
                    player.save()
                    return HttpResponse('<script type="text/javascript">window.close();window.opener.location.reload()</script>')
                else :
                    newregion.save()
                    if player.countdown == 2 :
                        player.countdown = 0
                    else :
                        player.countdown += 1
                    player.distance += 1
                    player.save()
                    return redirect("game:event")
                
            else :
                newregion.discovered = True
                if region.biome == "Spawn" :
                    Possibilities = random.choices(Nature, weights=[0,0,2,1,2], k = 10)
                    newregion.biome = random.choice(Possibilities)
                    Region.res(newregion,newregion.biome)
                    newregion.color = Colors[Nature.index(newregion.biome)]             
                elif region.biome == "Desert" :
                    Possibilities = random.choices(Nature, weights=[0,3,0,1,1], k = 10)
                    newregion.biome = random.choice(Possibilities)
                    Region.res(newregion,newregion.biome)
                    newregion.color = Colors[Nature.index(newregion.biome)]
                elif region.biome == "Aquatic" :
                    Possibilities = random.choices(Nature, weights=[3,0,0,1,1], k = 10)
                    newregion.biome = random.choice(Possibilities)
                    Region.res(newregion,newregion.biome)
                    newregion.color = Colors[Nature.index(newregion.biome)]
                elif region.biome == "Forest" :
                    Possibilities = random.choices(Nature, weights=[0,0,3,2,1], k = 10)
                    newregion.biome = random.choice(Possibilities)
                    Region.res(newregion,newregion.biome)
                    newregion.color = Colors[Nature.index(newregion.biome)]
                elif region.biome == "Mountain" :
                    Possibilities = random.choices(Nature, weights=[0,1,3,1,2], k = 10)
                    newregion.biome = random.choice(Possibilities)
                    Region.res(newregion,newregion.biome)
                    newregion.color = Colors[Nature.index(newregion.biome)]
                else :
                    if region.checkbuild():
                        Possibilities = random.choices(Nature, weights=[0,2,1,0,3], k = 10)
                        newregion.biome = random.choice(Possibilities)
                        Region.res(newregion,newregion.biome)
                        newregion.color = Colors[Nature.index(newregion.biome)]
                    else :
                        Possibilities = random.choices(Nature, weights=[2,2,1,0,3], k = 10)
                        newregion.biome = random.choice(Possibilities)
                        Region.res(newregion,newregion.biome)
                        newregion.color = Colors[Nature.index(newregion.biome)]
                player.distance += 1
                newregion.save()
                player.save()
                return redirect("game:event")
            for s in shelters :
                s.working()
        else :
            player.x = olx
            player.y = oly
            player.save()
            return HttpResponse('<script type="text/javascript">window.close();window.opener.location.reload()</script>')
    else :
        return render(request, 'game/map.html', context= { 'player' : player, 'world' : world})

# EVENT VIEW - open in the current window ( lock the player in the event until its resolution )
@login_required(login_url="/users/login")
def event(request):
    
    player = Player.objects.get(name=request.user.username)
    party = Party.objects.get(pplayer=player.pk)
    inventory = Inventory.objects.get(id=player.pinv_id)
    region = Region.objects.get(x=player.x,y=player.y)

    if player.occupied == "free" :
        event = Event.objects.get(id=random.randint(1,53))
        player.occupied = event.name
        player.save()
        if event.id == 28 or event.id == 29 or event.id == 41 or event.id == 42:
            if region.checkbuild() :
                return redirect("game:event")
            else :
                if event.name == "JOKER" :
                    return redirect("game:joker")
                else :
                    pass
    elif player.occupied == "fight" :
        return redirect("game:fight")
    else :
        event = Event.objects.get(name=player.occupied)
        pass

    if request.method == "POST":
        
        event = Event.objects.get(name=player.occupied)
        value = request.POST.get("reso")
        dice = random.randint(2, 12)

        if party.checkbonus(player,party,event.spe) :
            dice += 1
        elif party.checkmalus(player,party,event.mal) :
            dice -= 1
        else :
            pass

        if value == "fight" :   
            return redirect("game:fight")
        if value == "negociate" :
            dice = random.randint(2, 12)
            if party.checkbonus(player,party,"Charming") :
                dice += 1
                if dice > 9 :
                    event.resolution(player, party,inventory, "critss")
                elif dice > 6 :
                    event.resolution(player, party,inventory, "success")
                else :
                    event.resolution(player, party, inventory, "fail")
            elif party.checkmalus(player,party,"Ugly") :
                dice -= 1
                if dice > 9 :
                    event.resolution(player, inventory, "critss")
                elif dice > 6 :
                    event.resolution(player, inventory, "success")
                elif dice > 2 :
                    event.resolution(player, inventory, "fail")
                else :
                    event.resolution(player, inventory, "oups")
            else :
                if dice > 9 :
                    event.resolution(player, inventory, "critss")
                elif dice > 6 :
                    event.resolution(player, inventory, "success")
                elif dice > 2 :
                    event.resolution(player, inventory, "fail")
                else :
                    event.resolution(player, inventory, "oups")
        
        elif value == "flee" :
            dice = random.randint(2, 12)
            if party.checkbonus(player,party,"Discrete") :
                dice += 1
                if party.checkbonus(player,party,"Athletic") :
                    dice += 1
                else :
                    pass
                if dice < 6 :
                    event.resolution(player,party,inventory, "fail")
                else :
                    pass
            elif party.checkmalus(player,party,"Loud") :
                dice -= 1
                if party.checkmalus(player,party,"Asthmatic") :
                    dice -= 1
                else :
                    pass
                if dice < 6 :
                    event.resolution(player, party,inventory, "fail")
                elif dice < 3 :
                    event.resolution(player, party,inventory, "oups")
                else :
                    pass
            else :
                if dice < 6 :
                    event.resolution(player, party,inventory, "fail")
                elif dice < 3 :
                    event.resolution(player, party,inventory, "oups")
                else :
                    pass
        else :
            if event.power == 10 :
                if dice >= 10 :
                    event.resolution(player, party, inventory, "critss")
                elif dice >= 6 :
                    event.resolution(player, party, inventory, "success")
                elif dice >= 3 :
                    event.resolution(player, party, inventory, "fail")
                else :
                    event.resolution(player, party, inventory, "oups")
            elif event.power == 8 :
                if dice >= 8 :
                    event.resolution(player, party, inventory, "critss")
                elif dice >= 6 :
                    event.resolution(player, party, inventory, "success")
                elif dice >= 3 :
                    event.resolution(player, party, inventory, "fail")
                else :
                    event.resolution(player, party, inventory, "oups")
            elif event.power == 6 :
                if dice >= 6 :
                    event.resolution(player, party, inventory, "critss")
                elif dice >= 4 :
                    event.resolution(player, party, inventory, "success")
                elif dice > 2 :
                    event.resolution(player, party, inventory, "fail")
                else :
                    event.resolution(player, party, inventory, "oups")
            elif event.power == 4 :
                if dice >= 4 :
                    event.resolution(player, party, inventory, "critss")
                elif dice >= 3 :
                    event.resolution(player, party, inventory, "success")
                elif dice == 2 :
                    event.resolution(player, party, inventory, "fail")
                else :
                    event.resolution(player, party, inventory, "oups")
            elif event.power == 2 :
                if dice >= 6 :
                    event.resolution(player, party, inventory, "critss")
                elif dice >= 2 :
                    event.resolution(player, party, inventory, "success")
                else :
                    event.resolution(player, party, inventory, "fail")
            else :
                if event.type == "finding" and event == "PETS":
                    dice = random.randint(1,6)
                    if dice >= 12 :
                        event.resolution(player, party, inventory, "critss")
                    elif dice >= 8 :
                        event.resolution(player, party, inventory, "success")
                    elif dice >= 4 :
                        event.resolution(player, party, inventory, "fail")
                    else :
                        event.resolution(player, party, inventory, "oups")
                elif event.type == "finding" and event == "WRECKAGE" :
                    if dice >=12 :
                        event.resolution(player, party, inventory, "critss")
                    elif dice >= 8 :
                        event.resolution(player, party, inventory, "success")
                    elif dice >= 4 :
                        event.resolution(player, party, inventory, "fail")
                    else :
                        event.resolution(player, party, inventory, "oups")
                elif event.type == "finding" :
                    if dice > 2 :
                        event.resolution(player, party, inventory, "success")
                    else :
                        event.resolution(player, party, inventory, "fail")
                else :
                    if event.name == "MERCHANT" :
                        region.merchant = True
                    elif event.name == "DOCTOR" :
                        region.doctor = True
                    elif event.name == "DEALER" :
                        region.dealer = True
                    elif event.name == "ENGENEER" :
                        region.mecano = True
                    else :
                        pass
                    if dice >= 9 :
                        event.resolution(player, party, inventory, "critss")
                    elif dice > 2 :
                        event.resolution(player, party, inventory, "success")
                    else :
                        event.resolution(player, party, inventory, "fail")
        player.occupied = "free"
        if player.hp > 0 :
            player.luck += 1
        else :
            pass
        player.save()
        return HttpResponse('<script type="text/javascript">window.close();window.opener.location.reload()</script>')
    else :
        return render(request, 'game/event.html', context= { 'player' : player, 'event' : event, 'inventory' : inventory })  

# INVENTORY VIEW - open in a new window ( informative display only )
@login_required(login_url="/users/login")
def inventory(request):
    player = Player.objects.get(name=request.user.username)
    inventory = Inventory.objects.get(id=player.pinv_id)
    return render(request, 'game/inventory.html', context={ 'player' : player, 'inventory' : inventory })

# FARM VIEW - open in a new window
@login_required(login_url="/users/login")
def farm(request):
    player = Player.objects.get(name=request.user.username)
    party = Party.objects.get(pplayer=player.pk)
    region = Region.objects.get(x=player.x,y=player.y)
    if region.biome == "Spawn" or region.biome == "Camp" or region.biome == "Shelter" or region.biome == "Fortress":
        return HttpResponse('<script type="text/javascript">window.close()')
    else :
        pass
    playerinv = Inventory.objects.get(id=player.pinv_id)
    regioninv = Inventory.objects.get(id=region.rinv_id)
    

    if request.method == "POST":

        Res = [
            request.POST['food'],
            request.POST['wood'],
            request.POST['metal'],
            request.POST['fuel'],
        ]
        total = int(Res[0]) + int(Res[1]) + int(Res[2]) + int(Res[3])
        
        if total > Party.countmember(party) :
            player.journal = "not enough party members available !"
            player.save()
            return HttpResponse('<script type="text/javascript">window.close();window.opener.location.reload()</script>')
        elif player.tired :
            player.journal = "you are too tired to farm"
            player.save()
            return HttpResponse('<script type="text/javascript">window.close();window.opener.location.reload()</script>')
        else :
            food = int(Res[0]) * random.randint(2,3)
            wood = int(Res[1]) * random.randint(2,3)
            metal = int(Res[2]) * random.randint(1,3)
            fuel = int(Res[3]) * random.randint(1,3)
            playerinv.food += food
            playerinv.wood += wood
            playerinv.metal += metal
            playerinv.fuel += fuel
            playerinv.save()
            info = f'you found {food} food, {wood} wood, {metal} metal and {fuel} fuel.'
            player.journal = info
            player.tired = True
            player.save()
            if region.checkbuild():
                rng = random.randint(1,5)
                if rng == "5" :
                    return redirect("game:event")
                else :
                    return HttpResponse('<script type="text/javascript">window.close();window.opener.location.reload()</script>')
            else:
                rng = random.randint(1,3)
                if rng == "3" :
                    return redirect("game:event")
                else :
                    return HttpResponse('<script type="text/javascript">window.close();window.opener.location.reload()</script>')
    else :
        print("nothing append")
        return render(request, 'game/farm.html', context={ 'player': player, 'region' : region, 'inventory' : inventory })

# REST VIEW - open in a new window
@login_required(login_url="/users/login")
def rest(request):
    player = Player.objects.get(name=request.user.username)
    party = Party.objects.get(pplayer=player.pk)
    region = Region.objects.get(x=player.x,y=player.y)
    inventory = Inventory.objects.get(id=player.pinv_id)
    if request.method == "POST":
        if party.mem2 != 0 :
            mem2 = Player.objects.get(pk=party.mem2)
        else :
            mem2 = True
        if party.mem3 != 0 :
            mem3 = Player.objects.get(pk=party.mem3)
        else :
            mem3 = True
        if party.mem4 != 0 :
            mem4 = Player.objects.get(pk=party.mem4)
        else :
            mem4 = True
        if party.mem5 != 0 :
            mem5 = Player.objects.get(pk=party.mem5)
        else :
            mem5 = True
        if party.mem6 != 0 :
            mem6 = Player.objects.get(pk=party.mem6)
        else :
            mem6 = True
        if party.mem7 != 0 :
            mem7 = Player.objects.get(pk=party.mem7)
        else :
            mem7 = True

        anim = ["queen","horse","dog","cat"]
        if player.sick or player.wound or player.hp == 7 :
            pass
        else :
            player.hp += 1
        if mem2 :
            pass
        else :
            if mem2.name not in anim :
                if mem2.sick or mem2.wound or mem2.hp >= 7:
                    pass
                else :
                    mem2.hp += 1
                mem2.save()
            else :
                if mem2 == "queen" :
                    if mem5.hp < 10 :
                        mem2.hp += 1
                    else :
                        pass
                elif mem2 == "horse" :
                    if mem2.isck or mem2.wound or mem2.hp >= 5:
                        pass
                    else :
                        mem2.hp +=1
                else :
                    if mem2.isck or mem2.wound or mem2.hp >= 3:
                        pass
                    else :
                        mem2.hp +=1
                mem2.save()
        if mem3 :
            pass
        else :
            if mem3.name not in anim :
                if mem3.sick or mem3.wound or mem3.hp >= 7:
                    pass
                else :
                    mem3.hp += 1
                mem3.save() 
            else :
                if mem3 == "queen" :
                    if mem5.hp < 10 :
                        mem3.hp += 1
                    else :
                        pass
                elif mem3 == "horse" :
                    if mem3.isck or mem3.wound or mem3.hp >= 5:
                        pass
                    else :
                        mem3.hp +=1
                else :
                    if mem3.isck or mem3.wound or mem3.hp >= 3:
                        pass
                    else :
                                                mem3.hp +=1
                mem3.save()
        if mem4 :
            pass
        else :
            if mem4.name not in anim :
                if mem4.sick or mem4.wound or mem4.hp >= 7:
                    pass
                else :
                    mem4.hp += 1
                mem4.save()
            else :
                if mem4 == "queen" :
                    if mem5.hp < 10 :
                        mem4.hp += 1
                    else :
                        pass
                elif mem4 == "horse" :
                    if mem4.isck or mem4.wound or mem4.hp >= 5: 
                        pass
                    else :
                        mem4.hp +=1
                else :
                    if mem4.isck or mem4.wound or mem4.hp >= 3:
                        pass
                    else :
                        mem4.hp +=1
                mem4.save()
        if mem5 :
            pass
        else :
            if mem5.name not in anim :
                if mem5.sick or mem5.wound or mem5.hp >= 7:
                    pass
                else :
                    mem5.hp += 1
                mem5.save()
            else :
                if mem5 == "queen" :
                    if mem5.hp < 10 :
                        mem5.hp += 1
                    else :
                        pass
                elif mem5 == "horse" :
                    if mem5.isck or mem5.wound or mem5.hp >= 5:
                        pass
                    else :
                        mem5.hp +=1
                else :
                    if mem5.isck or mem5.wound or mem5.hp >= 3:
                        pass
                    else :
                        mem5.hp +=1
                mem5.save()
        if mem6 :
            pass
        else :
            if mem6.name not in anim :
                if mem6.sick or mem6.wound or mem6.hp >= 7:
                    pass
                else :
                    mem6.hp += 1
                mem6.save()
            else :
                if mem6 == "queen" :
                    if mem5.hp < 10 :
                        mem6.hp += 1
                    else :
                        pass
                elif mem6 == "horse" :
                    if mem6.isck or mem6.wound or mem6.hp >= 5:
                        pass
                    else :
                        mem6.hp +=1
                else :
                    if mem6.isck or mem6.wound or mem6.hp >= 3:
                        pass
                    else :
                        mem6.hp +=1
                mem6.save()
        if mem7 :
            pass
        else :
            if mem7.name not in anim :
                if mem7.sick or mem7.wound or mem7.hp >= 7:
                    pass
                else :
                    mem7.hp += 1
                mem7.save()
            else :
                if mem7 == "queen" :
                    if mem5.hp < 10 :
                        mem7.hp += 1
                    else :
                        pass
                elif mem7 == "horse" :
                    if mem7.isck or mem7.wound or mem7.hp >= 5:
                        pass
                    else :
                        mem7.hp +=1
                else :
                    if mem7.isck or mem7.wound or mem7.hp >= 3:
                        pass
                    else :
                        mem7.hp +=1
            mem7.save()
        player.journal = "your party rested for a while"
        player.tired = False
        player.save()
        return HttpResponse('<script type="text/javascript">window.close();window.opener.location.reload()</script>')
    else :
        return render(request, 'game/rest.html', context={ 'player': player, 'region' : region, 'inventory' : inventory,'party': party })

# FIGHT VIEW - open in the current window ( lock the player in a fightfield until end of fight )
@login_required(login_url="/users/login")
def fight(request):

    Region.autores()
    player = Player.objects.get(name=request.user.username)
    print(player.hp," when player object is uploaded ")
    inventory = Player.objects.get(pk=player.pinv)
    party = Party.objects.get(pplayer=player.pk)
    group = party.partylist()

    if player.occupied != "fight" :
        event = Event.objects.get(name=player.occupied)
        start = True
    else :
        if player.start :
            start = True
        else :
            start = False
        event = Event.objects.get(name="ANGRY MOB")

    player.occupied = "fight"
    check = FightField.objects.all().filter(name=player.name)

    if len(check) == 0 :

        FightField.versus(player)
        if event.power < 6 :
            n = 3
            while n > 0 :
                print("generating enemy")
                player.enemygen(event)
                n -= 1
        elif event.power < 10 :
            n = 2
            while n > 0 :
                player.enemygen(event)
                n -= 1
        else :
            player.enemygen(event)
        enemies = Player.objects.all().filter(name=player.pk)
        enem = list(Player.objects.all().filter(name=player.pk).values_list('pk',flat=True))
        FightField.placenemies(enemies)
        ff = FightField.objects.all().filter(name=player.name)

    else :

        enemies = Player.objects.all().filter(name=player.pk)
        enem = list(Player.objects.all().filter(name=player.pk).values_list('pk',flat=True))
        ff = FightField.objects.all().filter(name=player.name)

    if request.method == "POST":

        if request.POST.__contains__("pick"):

            keyc = request.POST['pick']
            char = Player.objects.get(pk=keyc)
            party.select(char,player)

            if request.POST.__contains__("action"):
                print("action in the datas")
                char.action = request.POST['action']
                print(char.name,char.action)
                if char.action == "defend" :
                    char.turn = False
                else :
                    pass
                char.save()
                print(char.action)
            else :
                pass

        elif request.POST.__contains__("action"):

            print("action in the datas")
            char = party.selected(player)
            char.action = request.POST['action']
            print(char.name,char.action)
            char.turn = False
            char.save()      
            print(char.action)

        else:

            print(request.POST)
            x = request.POST['x']
            y = request.POST['y']
            field = FightField.objects.get(x=x,y=y)
            print(field)
            if start :
                field.place(party.selected(player))
                partyl = party.partylist()
                if len(partyl) > 0 :
                    for m in partyl :
                        if m.start :
                            pass
                        else :
                            if player.start :
                                pass
                            else :
                                print("it's your turn")
                                player.turn = True
                                start = False
                                player.save()
                else :
                    player.turn = True
                    player.save()
                field.save()

            else :
                char = party.selected(player)
                previous = FightField.objects.get(char=char.pk)
                if char.action == "move" :
                    if previous.checkdist(field,char.speed) :
                        field.place(char)
                        previous.char = 0
                        previous.save()
                    else :
                        print("not possible")
                        pass
                elif char.action == "hit" :
                    if previous.checkdist(field,char.melee) :
                        print("à distance de melee")
                        victim = Player.objects.get(pk=field.char)
                        print(victim)
                        dmg = char.melee - victim.armor
                        print(char.melee," - ",victim.armor," = ",dmg,victim.hp)
                        if dmg < 0 :
                            pass
                        else :
                            victim.hp -= dmg
                        print(victim.hp)
                        if victim.hp <= 0 :
                            field.char = 0
                        else :
                            pass
                        victim.save()
                        char.turn = False
                    else :
                        pass
                elif char.action == "shoot" :
                    if previous.checkdist(field,char.range) :
                        if previous.aiming(char.aim) :
                            victim = Player.objects.get(pk=field.char)
                            dmg = char.melee - victim.armor
                            victim.hp -= dmg
                            if victim.hp <= 0 :
                                field.char = 0
                            else :
                                pass
                            victim.save()
                            char.turn = False
                        else :
                            pass
                    else :
                        pass
                else :
                    char.heal(1)
                    char.turn = False
                field.save()
                previous.save()
                char.save()

        if FightField.end(player,enem) :
            return redirect("game:loot")
        else :
            return redirect("game:fight")

    else :
        if start or party.checkturn(player) :
            turn = True
            return render(request, 'game/fight.html', context={ 'player': player, 'event' : event, 'inventory' : inventory , 'ff' : ff, 'member' : party, 'enem' : enem, 'group' : group, 'turn' : turn, 'start' : start })
        else :
            turn = False
            print(enemies," turn")
            for e in enemies :
                e.turn = True
                e.save()
            for e in enemies :
                if e.turn :
                    eff = FightField.objects.get(char=e.pk)
                    eff.goto(enemies)
                    print(player.hp," after enemy turn")
                else :
                    continue
            player.turn = True
            print(player.hp," before saving player turn True")
            player.save()
            partyl = party.partylist()
            for m in partyl :
                m.turn = True
                m.save()
            pass
            return redirect("game:fight")
            

# BUILD VIEW - open in a new window
@login_required(login_url="/users/login")
def build(request):
    player = Player.objects.get(name=request.user.username)
    party = Party.objects.get(pplayer=player.pk)
    region = Region.objects.get(x=player.x,y=player.y)
    regioninv = Inventory.objects.get(id=region.rinv_id)
    playerinv = Inventory.objects.get(id=player.pinv_id)
    shelters = 0
    for x in player.shelters :
        shelters += 1
    shelters += 1
    if request.method == "POST":
        if request.POST['build'] == "camp" :
            if playerinv.wood >= 50 and playerinv.food >= 50 and player.surv >= 20 :
                region.biome = "Camp"
                region.founder = player.name
                region.color = "saddlebrown"
                player.shelters = { shelters : region.pk }
                regioninv.coins = regioninv.coins + Region.resources(500,1000)
                regioninv.food = regioninv.food + Region.resources(100,250)
                regioninv.wood = regioninv.wood + Region.resources(100,250)
                regioninv.metal = regioninv.metal + Region.resources(50,100)
                regioninv.fuel = regioninv.fuel + Region.resources(0,25)
                regioninv.save()
                region.save()            
            else :
                player.journal = "not enough resources..."
                player.save()
        elif request.POST['build'] == "shelter" :
            if regioninv.wood >= 500 and regioninv.food >= 500 and regioninv.metal >= 200 and region.biome == "Camp" and region.surv >= 100 :
                if region.founder == player.name :
                    region.biome = "Shelter"
                    region.color = "slategrey"
                    regioninv.coins = regioninv.coins + Region.resources(1000,2500)
                    regioninv.food = regioninv.food + Region.resources(500,1000)
                    regioninv.wood = regioninv.wood + Region.resources(500,1000)
                    regioninv.metal = regioninv.metal + Region.resources(100,250)
                    regioninv.fuel = regioninv.fuel + Region.resources(50,100)
                    regioninv.save()
                    region.save()
                    player.save()
                else :
                    player.journal = "go home stranger !"
                    player.save()
            else :
                player.journal = "not enough resources..."
                player.save()
        else :
            if regioninv.wood >= 2500 and regioninv.food >= 2500 and regioninv.metal >= 1000 and region.biome == "Shelter" and region.surv >= 500 :
                if region.founder == player.name :
                    region.biome = "Fortress"
                    region.color = "darkslategrey"
                    regioninv.coins = regioninv.coins + Region.resources(2500,5000)
                    regioninv.food = regioninv.food + Region.resources(500,1000)
                    regioninv.wood = regioninv.wood + Region.resources(500,1000)
                    regioninv.metal = regioninv.metal + Region.resources(250,500)
                    regioninv.fuel = regioninv.fuel + Region.resources(100,250)
                    regioninv.save()
                    region.save()
                    player.save()
                else :
                    player.journal = "go home stranger !"
                    player.save()
            else :
                player.journal = "not enough resources..."
                player.save()
        return HttpResponse('<script type="text/javascript">window.close();window.opener.location.reload()</script>')
    else :  
        return render(request, 'game/build.html', context={ 'player': player, 'region' : region, 'playerinv' : playerinv, 'regioninv' : regioninv, 'party' : party  })

# SHELTER'S MANAGEMENT VIEW - open in the current window if player is the founder of the region he's in
@login_required(login_url="/users/login")
def manager(request):
    player = Player.objects.get(name=request.user.username)
    region = Region.objects.get(x=player.x,y=player.y)
    regioninv = Inventory.objects.get(id=region.rinv_id)
    playerinv = Inventory.objects.get(id=player.pinv_id)
    sector = region.scan()

    if request.method == "POST":
        Res = [
            request.POST['food'],
            request.POST['wood'],
            request.POST['metal'],
            request.POST['fuel'],
            request.POST['med'],
            request.POST['drug'],
            request.POST['katana'],
            request.POST['shotgun'],
            request.POST['armor'],
            request.POST['name']
        ]
        wlist = [
            request.POST['sfood'],
            request.POST['swood'],
            request.POST['smetal'],
            request.POST['sfuel']
        ]
        region.work(player,wlist)
        
    else :
        
        return render(request, 'game/manager.html', context={ 'player': player, 'region' : region, 'playerinv' : playerinv, 'regioninv' : regioninv, 'sector' : sector })

# JOKER VIEW - special event that allows the player to chose between all events
@login_required(login_url="/users/login")
def joker(request):
    player = Player.objects.get(name=request.user.username)
    allev = Event.objects.all()
    return render(request, 'game/joker.html', context= { 'player' : player, 'allev' : allev})

# DEATH VIEW - open in current window if player's health is <= 0
def rip(request):
    player = Player.objects.get(name=request.user.username)
    if request.method == "POST":
        print("deleting player...")
        player.delete()
        return redirect("users:logout")
    else :
        return render(request, 'game/rip.html', context= { 'player' : player })