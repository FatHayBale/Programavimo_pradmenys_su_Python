
import random
import time


def story(text, delay=0.012):
    for character in text:
        print(character, end="", flush=True)
        time.sleep(delay)
    print()


class Item:
    def __init__(self, name, description, item_type="misc", location="room", magical=False, value=1):
        self.name = name
        self.description = description
        self.item_type = item_type
        self.location = location
        self.magical = magical
        self.value = value
        self.tags = []

    def describe(self):
        return f"{self.name}: {self.description}"

    def describe_location(self):
        return f"{self.name} is in {self.location}."


class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        if item is None:
            story("That item doesn't exist.")
            return False

        if item in self.items or self.has_item(item.name) is not None:
            story(f"You already have {item.name}.")
            return False

        self.items.append(item)
        item.location = "inventory"
        return True

    def remove_item(self, item):
        if item is None:
            story("That item doesn't exist.")
            return False

        if item in self.items:
            self.items.remove(item)
            item.location = "ground"
            return True

        story(f"{item.name} is not in your inventory.")
        return False

    def has_item(self, item_name):
        for item in self.items:
            if item.name.lower() == item_name.lower():
                return item
        return None

    def show_items(self):
        if not self.items:
            story("Your inventory is empty.")
            return []

        story("Inventory:")
        for index, item in enumerate(self.items, start=1):
            story(f"{index}. {item.name} - {item.description} (value: {item.value} gold)")
        return self.items

    def drop_item(self, item, room=None):
        if item is None:
            story("You cannot drop nothing.")
            return False

        if item in self.items:
            self.items.remove(item)
            if room is not None:
                room.add_item(item)
            else:
                item.location = "ground"
            story(f"You drop the {item.name} on the floor.")
            return True

        story(f"You do not have {item.name}.")
        return False

    def combine_items(self, first_item, second_item):
        if first_item is None or second_item is None:
            story("You need two valid items to combine.")
            return None

        if first_item not in self.items or second_item not in self.items:
            story("Both items must be in your inventory.")
            return None

        if first_item.name == second_item.name:
            story("You cannot combine an item with itself.")
            return None

        recipe = {first_item.name.lower(), second_item.name.lower()}
        recipes = {
            frozenset({"emberroot", "silver oil"}): Item(
                "Ember Tonic",
                "A glowing red tonic that steadies the body and sharpens the mind.",
                item_type="consumable",
                value=22,
            ),
            frozenset({"flask of poison", "smoke bomb"}): Item(
                "Poison Bomb",
                "A smoke bomb packed with venomous powder.",
                item_type="bomb",
                magical=True,
                value=38,
            ),
            frozenset({"moonglass shard", "silver oil"}): Item(
                "Moon Oil",
                "A pale oil that makes a weapon bite through dark armor.",
                item_type="oil",
                magical=True,
                value=42,
            ),
        }
        result = recipes.get(frozenset(recipe))
        if result is None:
            story(f"You try to combine {first_item.name} and {second_item.name}, but nothing useful happens.")
            return None

        self.remove_item(first_item)
        self.remove_item(second_item)
        self.add_item(result)
        story(f"You combine {first_item.name} and {second_item.name} and create {result.name}.")
        return result


class Player:
    def __init__(self, health, clothes, role="wanderer"):
        self.health = health
        self.max_health = health
        self.inventory = Inventory()
        self.clothes = clothes
        self.role = role
        self.gold = 30
        self.strength = 10
        self.agility = 9
        self.luck = 8
        self.weapon_skill = 10
        self.weapon = None

        if role == "warrior":
            self.max_health = 115
            self.health = self.max_health
            self.strength = 13
            self.weapon_skill = 12
        elif role == "scout":
            self.agility = 14
            self.luck = 11
        elif role == "alchemist":
            self.luck = 12
            self.max_health = 90
            self.health = self.max_health

    def add_item(self, item):
        if not self.inventory.add_item(item):
            return False
        if item.item_type == "weapon" and self.weapon is None:
            self.weapon = item
        return True

    def describe_role(self):
        role_text = {
            "warrior": "strong and durable",
            "scout": "quick and lucky",
            "alchemist": "skilled with strange ingredients",
            "wanderer": "balanced and untested",
        }
        story(f"You are a {self.role}: {role_text.get(self.role, 'hard to predict')}.")
        story(f"Health: {self.health}/{self.max_health}, Gold: {self.gold}")

    def pickup_item(self, item, room):
        if item is None:
            story("That item doesn't exist.")
            return False

        if item not in room.items:
            story(f"{item.name} is not in this room.")
            return False

        if not self.add_item(item):
            return False
        room.remove_item(item)
        story(f"You picked up {item.name}.")
        return True

    def show_inventory(self):
        return self.inventory.show_items()

    def open_inventory(self):
        return self.show_inventory()

    def combine_items(self, first_item, second_item):
        return self.inventory.combine_items(first_item, second_item)

    def drop_item(self, item, room):
        if item is self.weapon:
            self.weapon = None
        return self.inventory.drop_item(item, room)

    def use_bomb(self, enemy):
        bomb = self.inventory.has_item("Poison Bomb")
        if bomb is None:
            bomb = self.inventory.has_item("Smoke Bomb")
        if bomb is None:
            story("You do not have a bomb.")
            return False

        self.inventory.remove_item(bomb)
        damage = random.randint(18, 30)
        enemy.health -= damage
        story(f"You throw the {bomb.name}. It bursts in a cloud of smoke and deals {damage} damage.")
        return True

    def use_health_potion(self):
        potion = self.inventory.has_item("Healing Potion")
        if potion is None:
            story("You have no Healing Potion.")
            return False

        self.inventory.remove_item(potion)
        heal_amount = random.randint(24, 36)
        self.health = min(self.max_health, self.health + heal_amount)
        story(f"You drink the Healing Potion and recover {heal_amount} health.")
        story(f"Your health is now {self.health}/{self.max_health}.")
        return True

    def use_herb(self, herb_name="Emberroot"):
        herb = self.inventory.has_item(herb_name)
        if herb is None:
            story(f"You do not have {herb_name}.")
            return False

        self.inventory.remove_item(herb)
        heal_amount = random.randint(8, 16)
        self.health = min(self.max_health, self.health + heal_amount)
        self.luck += 1
        story(f"You chew the {herb_name} and feel the bitter warmth settle into your nerves.")
        story(f"You recover {heal_amount} health and your luck sharpens a little.")
        return True

    def use_ember_tonic(self):
        tonic = self.inventory.has_item("Ember Tonic")
        if tonic is None:
            story("You do not have an Ember Tonic.")
            return False

        self.inventory.remove_item(tonic)
        self.strength += 2
        self.weapon_skill += 2
        story("You drink the Ember Tonic. Heat spreads through your arms and your grip becomes certain.")
        story("Your strength and weapon skill increase by 2.")
        return True

    def brew_potion(self, cauldron):
        if cauldron is None:
            story("There is no cauldron to brew in.")
            return False

        emberroot = self.inventory.has_item("Emberroot")
        silver_oil = self.inventory.has_item("Silver Oil")
        if emberroot is None or silver_oil is None:
            story("The cauldron needs Emberroot and Silver Oil before it can brew a useful tonic.")
            return False

        self.inventory.remove_item(emberroot)
        self.inventory.remove_item(silver_oil)
        tonic = Item("Ember Tonic", "A glowing red tonic that steadies the body and sharpens the mind.", item_type="consumable", value=22)
        self.inventory.add_item(tonic)
        story("You drop the Emberroot and Silver Oil into the cauldron. It boils violently and then settles into a warm red tonic.")
        story("You brew an Ember Tonic.")
        return True

    def try_to_flee(self, enemy):
        flee_roll = random.randint(1, 20) + self.agility + self.luck
        enemy_roll = random.randint(1, 20) + enemy.agility + enemy.luck

        if flee_roll >= enemy_roll:
            story("You slip away into the shadows before the enemy can finish the strike.")
            return True

        story(f"You try to run, but the {enemy.name} cuts you off and lunges forward.")
        enemy.counter_attack(self)
        return False

    def dip_weapon_in_cauldron(self, cauldron):
        if self.weapon is None:
            story("You have no weapon to dip.")
            return False

        if not cauldron.is_ready_for_weapon:
            story("The cauldron is not ready for your blade.")
            return False

        self.weapon.tags.append("poisoned")
        self.weapon.magical = True
        story(f"You dip your {self.weapon.name} into the cauldron and the steel turns sickly green.")
        story("The blade hums with a poison-laced curse.")
        return True

    def attack(self, enemy, verb="slash"):
        attack_roll = random.randint(1, 20) + self.strength + self.weapon_skill + self.agility
        defense_roll = enemy.agility + enemy.luck + enemy.armor
        total = attack_roll - defense_roll

        if total <= 0:
            failure_strings = [
                "you stumble on rough ground and almost fall flat",
                "your footing breaks and you swing wildly past the target",
                "you overcommit and leave yourself open to a terrible mistake",
                "your blade catches the air instead of flesh",
                "you misjudge the distance and nearly throw yourself off balance",
            ]
            fail_phrase = random.choice(failure_strings)
            self_story = random.choice([
                "You try to {verb} the {enemy_name}, but {fail_phrase}.",
                "You lunge in an attempt to {verb} the {enemy_name}, but {fail_phrase}.",
                "You go for a {verb}, but {fail_phrase}.",
            ])
            story(self_story.format(verb=verb, enemy_name=enemy.name, fail_phrase=fail_phrase), delay=0.025)
            enemy.counter_attack(self)
            return False

        if total <= 6:
            damage = random.randint(4, 10)
            if "poisoned" in getattr(self.weapon, "tags", []):
                damage += 3
            enemy.health = max(0, enemy.health - damage)
            enemy_story = random.choice([
                "The strike bites into the {enemy_name}'s side, leaving a shallow but ugly cut.",
                "You land a decent hit and the {enemy_name} staggers backward.",
                "Your {verb} lands, drawing blood and forcing the enemy to recoil.",
            ])
            story(enemy_story.format(enemy_name=enemy.name, verb=verb), delay=0.028)
            story(f"You deal {damage} damage. The {enemy.name} has {enemy.health}/{enemy.max_health} health left.")
            return enemy.health <= 0

        damage = random.randint(11, 19)
        if "poisoned" in getattr(self.weapon, "tags", []):
            damage += 5
        enemy.health = max(0, enemy.health - damage)
        crit_story = random.choice([
            "Your {verb} is perfect. Steel flashes through the air and cuts deep into the {enemy_name}'s body.",
            "The attack lands with brutal precision. The {enemy_name} reels, stunned and bleeding badly.",
            "You drive your strike home and the enemy stumbles, gasping in pain.",
        ])
        story(crit_story.format(enemy_name=enemy.name, verb=verb), delay=0.028)
        story(f"You deal {damage} damage. The {enemy.name} has {enemy.health}/{enemy.max_health} health left.")
        return enemy.health <= 0


class Enemy:
    def __init__(self, name, weapon, health, max_health, strength, agility, luck, armor, description):
        self.name = name
        self.weapon = weapon
        self.health = health
        self.max_health = max_health
        self.strength = strength
        self.agility = agility
        self.luck = luck
        self.armor = armor
        self.description = description
        self.inventory = []
        self.phase = 1
        self.is_boss = False

    @classmethod
    def create_random(cls):
        names = ["Goblin", "Bandit", "Raider", "Wolfman", "Marauder", "Skeleton", "Thorn Knight"]
        weapons = ["rusted sword", "iron axe", "long spear", "cracked staff", "bite and claws", "bone club"]
        titles = [
            "a crooked hunter",
            "a bloodthirsty bruiser",
            "a hungry raider",
            "a twitchy skirmisher",
            "a savage predator",
        ]

        name = random.choice(names)
        weapon = random.choice(weapons)
        strength = random.randint(6, 16)
        agility = random.randint(5, 15)
        luck = random.randint(3, 14)
        armor = random.randint(1, 7)
        max_health = random.randint(28, 58) + strength
        health = max_health
        description = f"{name} is {random.choice(titles)} carrying a {weapon}."

        return cls(name, weapon, health, max_health, strength, agility, luck, armor, description)

    def counter_attack(self, player):
        damage = random.randint(6, 16) + self.strength - player.agility // 4
        if self.is_boss and self.phase == 2:
            damage += 5
        guard_charm = player.inventory.has_item("Guard Charm")
        if guard_charm is not None:
            player.inventory.remove_item(guard_charm)
            damage //= 2
            story("Your Guard Charm flashes and turns the enemy's first clean hit into a glancing blow.")
        damage = max(3, damage)
        player.health = max(0, player.health - damage)
        swing_lines = [
            f"The {self.name} whips the {self.weapon} around and cracks you across the side.",
            f"The {self.name} lunges in with brutal force, driving the {self.weapon} into your guard.",
            f"A furious strike from the {self.name} lands hard, and you feel your bones rattle.",
            f"The {self.name} steps in and crashes the {self.weapon} down with terrible momentum.",
        ]
        story(random.choice(swing_lines), delay=0.028)
        story(f"You take {damage} damage. Your health is now {player.health}/{player.max_health}.")

    @classmethod
    def create_boss(cls):
        boss = cls(
            "Ashen Warden",
            "a great black halberd",
            125,
            125,
            18,
            13,
            12,
            8,
            "A towering knight wrapped in ash and old iron. A red light burns behind its visor.",
        )
        boss.is_boss = True
        boss.inventory = [Item("Warden's Heart", "A warm black crystal that pulses like a second heart.", item_type="relic", magical=True, value=90)]
        return boss

    def describe(self):
        story(self.description)
        story(f"Health: {self.health}/{self.max_health}")
        story(f"Strength: {self.strength}, Agility: {self.agility}, Luck: {self.luck}, Armor: {self.armor}")


class Interactable:
    def __init__(self, name, description, kind, is_ready=False):
        self.name = name
        self.description = description
        self.kind = kind
        self.is_ready = is_ready
        self.is_ready_for_weapon = is_ready

    def inspect(self):
        story(self.description)


class GoblinShop:
    def __init__(self, stock):
        self.name = "Goblin Shop"
        self.description = "A one-eyed goblin has arranged useful goods on a blanket and watches you with professional suspicion."
        self.kind = "shop"
        self.stock = stock

    def inspect(self):
        story(self.description)
        story("The goblin's stock:")
        for item in self.stock:
            story(f"- {item.name}: {item.value} gold")

    def buy(self, player, item_name):
        for item in self.stock:
            if item.name.lower() == item_name.lower():
                if player.gold < item.value:
                    story("The goblin taps the price tag. You do not have enough gold.")
                    return False
                if not player.add_item(item):
                    story("You cannot carry another copy of that item.")
                    return False
                player.gold -= item.value
                self.stock.remove(item)
                story(f"You buy the {item.name} for {item.value} gold. You have {player.gold} gold left.")
                return True
        story("The goblin does not have that item in stock.")
        return False

    def sell(self, player, item_name):
        item = player.inventory.has_item(item_name)
        if item is None:
            story("You do not have that item.")
            return False
        if item.item_type == "key":
            story("The goblin refuses to buy a key. It has too many enemies already.")
            return False
        if item is player.weapon:
            story("The goblin will not buy the weapon you are currently using.")
            return False
        sale_value = max(1, item.value // 2)
        player.inventory.remove_item(item)
        player.gold += sale_value
        self.stock.append(item)
        story(f"The goblin buys your {item.name} for {sale_value} gold. You have {player.gold} gold.")
        return True


class Room:
    def __init__(self, name, description, items, enemies=None, directions=None, connected_rooms=None, cleared=False, interactables=None, locked=False, required_key=None):
        self.name = name
        self.description = description
        self.items = items if items is not None else []
        self.enemy = enemies if enemies is not None else []
        self.directions = directions if directions is not None else []
        self.connected_rooms = connected_rooms if connected_rooms is not None else []
        self.cleared = cleared
        self.interactables = interactables if interactables is not None else []
        self.locked = locked
        self.required_key = required_key

        for item in self.items:
            item.location = self.name

    def add_item(self, item):
        if item is None:
            story("That item can't be added.")
            return False

        if item not in self.items:
            self.items.append(item)
            item.location = self.name
            return True

        story(f"{item.name} is already in this room.")
        return False

    def remove_item(self, item):
        if item is None:
            story("That item doesn't exist in this room.")
            return False

        if item in self.items:
            self.items.remove(item)
            item.location = "ground"
            return True

        story("That item doesn't exist in this room.")
        return False

    def show_items(self):
        if not self.items:
            story(f"There are no items in {self.name}.")
            return []

        story(f"Items in {self.name}:")
        for index, item in enumerate(self.items, start=1):
            story(f"{index}. {item.name} - {item.description}")
        return self.items

    def room_actions(self):
        actions = []
        for item in self.items:
            actions.append(f"Pick up {item.name}")
        actions.append("Open inventory")
        for interactable in self.interactables:
            actions.append(f"Use {interactable.name}")
        for direction in self.directions:
            if direction == "locked":
                actions.append("Locked door")
            else:
                actions.append(f"Go {direction}")
        for enemy in self.enemy:
            actions.append(f"Fight {enemy.name}")
        if self.cleared:
            actions.append("Room cleared")
        return actions


class BattleEngine:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

    def check_critical_moment(self):
        has_potion = self.player.inventory.has_item("Healing Potion") is not None
        has_bomb = self.player.inventory.has_item("Poison Bomb") is not None or self.player.inventory.has_item("Smoke Bomb") is not None

        if self.player.health <= 35 and (has_potion or has_bomb):
            choice = input("Your health is critical. Use a potion, bomb, flee, or keep fighting? [potion/bomb/flee/fight]: ").strip().lower()
            if choice.startswith("p"):
                self.player.use_health_potion()
            elif choice.startswith("b"):
                self.player.use_bomb(self.enemy)
            elif choice.startswith("f"):
                if self.player.try_to_flee(self.enemy):
                    story("You escape the battle.")
                    return "fled"
                return "continue"
            return "continue"

        if self.player.health <= 20:
            choice = input("You are in serious danger. Use a potion, bomb, flee, or risk it? [potion/bomb/flee/fight]: ").strip().lower()
            if choice.startswith("p"):
                self.player.use_health_potion()
            elif choice.startswith("b"):
                self.player.use_bomb(self.enemy)
            elif choice.startswith("f"):
                if self.player.try_to_flee(self.enemy):
                    story("You escape the battle.")
                    return "fled"
                return "continue"
            return "continue"

        return "continue"

    def run(self):
        story(f"A {self.enemy.name} steps out of the dark.")
        story(self.enemy.description)
        story(f"The {self.enemy.name} has {self.enemy.health} health.")

        while self.player.health > 0 and self.enemy.health > 0:
            if self.enemy.is_boss and self.enemy.phase == 1 and self.enemy.health <= self.enemy.max_health // 2:
                self.enemy.phase = 2
                self.enemy.strength += 4
                self.enemy.armor += 2
                story("The Ashen Warden cracks its own armor and releases a storm of burning ash.")
                story("Phase two begins. Its attacks become faster and far more dangerous.")

            player_action = random.choice(["slash", "stab", "smash", "cut", "strike", "lunge"])
            if self.player.attack(self.enemy, player_action):
                story(f"You struck the final blow. The {self.enemy.name} collapses to the ground.")
                break

            if self.enemy.health <= 0:
                break

            if self.player.health <= 0:
                story("You collapse in a pool of blood. The story ends here.")
                break

            critical = self.check_critical_moment()
            if critical == "fled":
                break

            if self.enemy.health > 0 and self.player.health > 0:
                story(f"The {self.enemy.name} snarls and readies another attack.")

        if self.player.health <= 0:
            story("You are dead. The adventure ends in silence.")
        elif self.enemy.health <= 0:
            story(f"Victory. The {self.enemy.name} falls, and the battle is yours.")


def build_world():
    sword = Item("Iron Sword", "A practical blade with a well-worn grip.", item_type="weapon", value=28)
    potion = Item("Healing Potion", "A bright red potion that mends broken flesh.", item_type="consumable", value=18)
    flask_of_poison = Item("Flask of Poison", "A green glass flask, heavy with bitter venom.", item_type="consumable", magical=True, value=25)
    torch = Item("Torch", "A wooden torch that gives a warm, flickering light.", item_type="tool", value=5)
    rusted_key = Item("Rusted Key", "A key of black iron, worn smooth by years of use.", item_type="key", value=12)
    silver_oil = Item("Silver Oil", "A slick oil that glows faintly in moonlight.", item_type="oil", value=16)
    emberroot = Item("Emberroot", "A smoldering root that smells of smoke and rain.", item_type="herb", value=10)
    moonglass = Item("Moonglass Shard", "A clear shard that hums softly in your palm.", item_type="relic", value=35)
    iron_key = Item("Iron Key", "A key carved from pale iron, heavy with old magic.", item_type="key", value=20)
    smoke_bomb = Item("Smoke Bomb", "A clay sphere that can turn a bad moment into an escape.", item_type="tool", value=20)
    guard_charm = Item("Guard Charm", "A small charm that makes an enemy's first strike feel slower.", item_type="relic", magical=True, value=32)

    cauldron = Interactable(
        "Cauldron",
        "A black iron cauldron bubbles with a strange green broth. It looks like it could be used to brew potions or coat metal.",
        "cauldron",
        True,
    )
    shrine = Interactable(
        "Shrine",
        "A cracked stone shrine is lined with tiny candles. The air tastes metallic and old.",
        "shrine",
        False,
    )
    forge = Interactable(
        "Forge",
        "The forge still glows with the last heat of a forgotten smith, and a bucket of quenching water sits nearby.",
        "forge",
        False,
    )
    loose_wall = Interactable(
        "Loose Wall",
        "One section of the cellar wall is newer than the rest. A draft slips through its cracks.",
        "secret",
        False,
    )
    mirror = Interactable(
        "Black Mirror",
        "The mirror reflects the room a few seconds late. Something small moves behind your reflection.",
        "secret",
        False,
    )
    altar = Interactable(
        "Ash Altar",
        "A low altar bears a hollow shaped like a heart. It seems to be waiting for something.",
        "altar",
        False,
    )
    goblin_shop = GoblinShop([
        Item("Healing Potion", "A bright red potion that mends broken flesh.", item_type="consumable", value=18),
        Item("Smoke Bomb", "A clay sphere that can turn a bad moment into an escape.", item_type="tool", value=20),
        Item("Guard Charm", "A small charm that makes an enemy's first strike feel slower.", item_type="relic", magical=True, value=32),
    ])

    entrance = Room(
        "Damp Entrance",
        "You stand in a damp stone hall where the walls drip with cold moisture. Loose bricks and old bones line the floor.",
        [torch],
        [],
        ["Ashen Cellar", "Moonwell Chapel"],
        [],
        False,
        [cauldron, goblin_shop],
    )

    cellar = Room(
        "Ashen Cellar",
        "A low, smoky cellar breathes with old heat. Iron tools hang from hooks and a hidden shrine waits beneath the dust.",
        [emberroot, silver_oil],
        [Enemy.create_random()],
        ["Damp Entrance", "Bone Crypt"],
        [],
        False,
        [forge, shrine, loose_wall],
    )

    crypt = Room(
        "Bone Crypt",
        "The crypt smells of mildew and old death. A stone altar sits under a broken arch, and a rusted key hangs from a chain.",
        [rusted_key],
        [Enemy.create_random()],
        ["Ashen Cellar", "Moonwell Chapel"],
        [],
        False,
        [mirror],
        locked=False,
        required_key=None,
    )

    chapel = Room(
        "Moonwell Chapel",
        "The chapel is lit by pale blue light, spilling from a cracked basin in the center. It feels as if the very stone is listening.",
        [moonglass, flask_of_poison],
        [Enemy.create_random()],
        ["Damp Entrance", "Bone Crypt", "Sanctum of Ash"],
        [],
        False,
        [cauldron, altar],
        locked=True,
        required_key=rusted_key,
    )

    boss_room = Room(
        "Sanctum of Ash",
        "At the far end of the dungeon, a ruined sanctum hums with unnatural stillness. A great iron door stands half-open, waiting for the right key.",
        [],
        [Enemy.create_boss()],
        ["Moonwell Chapel"],
        [altar],
        False,
        [],
        locked=True,
        required_key=iron_key,
    )

    secret_room = Room(
        "Smuggler's Nook",
        "A cramped hidden room packed with old crates. Someone used this place to move contraband beneath the dungeon.",
        [smoke_bomb, guard_charm, iron_key],
        [Enemy.create_random()],
        ["Ashen Cellar"],
        [],
        False,
        [],
    )

    return [entrance, cellar, crypt, chapel, boss_room, secret_room], {
        "sword": sword,
        "potion": potion,
        "torch": torch,
        "rusted_key": rusted_key,
        "silver_oil": silver_oil,
        "emberroot": emberroot,
        "moonglass": moonglass,
        "flask_of_poison": flask_of_poison,
        "iron_key": iron_key,
        "smoke_bomb": smoke_bomb,
        "guard_charm": guard_charm,
    }


def normalize_name(value):
    return " ".join(str(value).strip().lower().split())


def build_room_lookup(rooms):
    lookup = {}
    for room in rooms:
        name = normalize_name(room.name)
        lookup[name] = room
        parts = name.split()
        for word in parts:
            lookup[word] = room
        for index in range(1, len(parts)):
            lookup[" ".join(parts[index:])] = room
    return lookup


def resolve_room(target_name, room_map, current_room):
    normalized = normalize_name(target_name)
    if not normalized:
        return None

    if normalized in room_map:
        return room_map[normalized]

    for direction in current_room.directions:
        if normalize_name(direction) == normalized:
            return room_map.get(normalize_name(direction))

    for room in room_map.values():
        if normalize_name(room.name) == normalized:
            return room

    return None


def can_travel(current_room, target_room):
    if target_room is None:
        return False

    for direction in current_room.directions:
        if normalize_name(direction) == normalize_name(target_room.name):
            return True

    return False


def ending(player):
    story("You stand in the quiet dungeon and realize that everything went exactly as planned.")
    story("You feel happy, fulfilled, and quietly proud of yourself.")
    story("Then your foot lands on a banana peel.")

    has_sharp_item = player.weapon is not None
    for item in player.inventory.items:
        if item.item_type == "weapon":
            has_sharp_item = True

    if has_sharp_item:
        story("Unfortunately, you brought something sharp. The fall leaves you badly injured, and the adventure ends in an unnecessarily avoidable lesson.")
    else:
        story("Luckily, you have nothing sharp nearby. You survive the fall, embarrassed but completely unharmed.")
    story("The End.")


def main():
    rooms, items = build_world()
    room_map = build_room_lookup(rooms)
    story("Choose your role: warrior, scout, alchemist, or wanderer.")
    role = input("> ").strip().lower()
    if role not in {"warrior", "scout", "alchemist", "wanderer"}:
        role = "wanderer"
    player = Player(100, "peasant_clothes", role)
    player.add_item(items["sword"])
    player.add_item(items["potion"])

    current_room = room_map["damp entrance"]
    story(current_room.description)
    story(f"You stand in the {current_room.name}.")
    player.describe_role()
    story("A low, uneasy feeling settles in your bones.")
    story("You can feel the dungeon breathe around you.")
    story("Type 'help' to see the commands.")

    running = True
    while running:
        if player.health <= 0:
            story("You collapse before the dungeon can finish with you.")
            break

        if current_room.enemy:
            story(f"A {current_room.enemy[0].name} lingers in the room. The air is tense.")

        story("\nAvailable exits: " + ", ".join(current_room.directions) if current_room.directions else "None")
        story("What do you do?")
        command = input("> ").strip().lower()

        if command in {"", "wait"}:
            story("You hold your breath and listen to the dungeon breathe.")
            continue

        if command in {"quit", "exit", "leave"}:
            story("You turn away from the dungeon and leave the story unfinished.")
            running = False
            continue

        if command in {"help", "?"}:
            story("Commands: look, inventory, profile, go <room>, take <item>, use <object>, shop, buy <item>, sell <item>, fight, help, quit")
            continue

        if command in {"look", "l", "inspect"}:
            story(current_room.description)
            if current_room.items:
                story("You see:")
                for item in current_room.items:
                    story(f"- {item.name}: {item.description}")
            if current_room.interactables:
                story("Interactive objects:")
                for obj in current_room.interactables:
                    story(f"- {obj.name}: {obj.description}")
            continue

        if command in {"inventory", "inv", "i"}:
            player.show_inventory()
            continue

        if command in {"profile", "stats", "role"}:
            player.describe_role()
            continue

        if command in {"shop", "trade"}:
            shop = None
            for obj in current_room.interactables:
                if getattr(obj, "kind", "") == "shop":
                    shop = obj
                    break
            if shop is None:
                story("There is no shop here.")
            else:
                shop.inspect()
                story(f"You have {player.gold} gold.")
            continue

        if command.startswith("buy ") or command.startswith("sell "):
            action, item_name = command.split(" ", 1)
            shop = None
            for obj in current_room.interactables:
                if getattr(obj, "kind", "") == "shop":
                    shop = obj
                    break
            if shop is None:
                story("There is no goblin shop here.")
            elif action == "buy":
                shop.buy(player, item_name)
            else:
                shop.sell(player, item_name)
            continue

        if command.startswith("go "):
            target_name = command[3:].strip()
            if not target_name:
                story("Go where?")
                continue

            target_room = resolve_room(target_name, room_map, current_room)
            if target_room is None:
                story(f"You cannot go to {target_name} from here.")
                continue

            if not can_travel(current_room, target_room):
                story(f"There is no path leading {target_name} from here.")
                continue

            if target_room.locked:
                if target_room.required_key is None:
                    story("The door is barred shut.")
                    continue

                if player.inventory.has_item(target_room.required_key.name) is None:
                    story(f"The door is locked. You need the {target_room.required_key.name}.")
                    continue

                story(f"You unlock the door with the {target_room.required_key.name}.")
                target_room.locked = False

            current_room = target_room
            story(f"You move into the {current_room.name}.")
            story(current_room.description)
            continue

        if command.startswith("take ") or command.startswith("pick up "):
            item_name = command.split(" ", 2)[-1].strip()
            item = None
            for room_item in current_room.items:
                if room_item.name.lower() == item_name.lower():
                    item = room_item
                    break

            if item is None:
                story(f"There is no {item_name} in this room.")
                continue

            player.pickup_item(item, current_room)
            continue

        if command.startswith("use "):
            target_name = command[4:].strip()
            lower_name = target_name.lower()

            if lower_name in {"healing potion", "potion"}:
                player.use_health_potion()
                continue

            if lower_name in {"emberroot", "herb"}:
                player.use_herb()
                continue

            if lower_name in {"ember tonic", "tonic"}:
                player.use_ember_tonic()
                continue

            if lower_name == "cauldron":
                cauldron = None
                for obj in current_room.interactables:
                    if obj.name.lower() == "cauldron":
                        cauldron = obj
                        break
                if cauldron is None:
                    story("There is no cauldron here.")
                    continue

                poison = player.inventory.has_item("Flask of Poison")
                emberroot = player.inventory.has_item("Emberroot")
                silver_oil = player.inventory.has_item("Silver Oil")

                if poison is not None and emberroot is not None and silver_oil is not None:
                    story("You pour the ingredients into the cauldron. The contents rise and then settle into a bright, dangerous tonic.")
                    player.brew_potion(cauldron)
                elif poison is not None:
                    story("You pour the Flask of Poison into the cauldron. It bubbles with a green, sickly hiss.")
                    cauldron.is_ready = True
                    cauldron.is_ready_for_weapon = True
                    player.inventory.remove_item(poison)
                elif emberroot is not None and silver_oil is not None:
                    player.brew_potion(cauldron)
                elif player.weapon is not None:
                    if cauldron.is_ready_for_weapon:
                        player.dip_weapon_in_cauldron(cauldron)
                    else:
                        story("The cauldron is quiet. It needs a stronger ingredient before your weapon can be dipped.")
                else:
                    story("The cauldron bubbles but there is nothing worthy of dipping here.")
                continue

            if lower_name in {"loose wall", "wall", "secret passage"}:
                if current_room.name != "Ashen Cellar":
                    story("There is no loose wall here.")
                    continue
                if "Smuggler's Nook" not in current_room.directions:
                    current_room.directions.append("Smuggler's Nook")
                    current_room.interactables = [obj for obj in current_room.interactables if obj.name != "Loose Wall"]
                    story("You press the loose stone. The wall folds inward, revealing a narrow passage.")
                    story("A hidden room has been discovered.")
                else:
                    story("The secret passage is already open.")
                continue

            if lower_name in {"black mirror", "mirror"}:
                if current_room.name != "Bone Crypt":
                    story("There is no black mirror here.")
                    continue
                story("Your reflection turns its head before you do. Behind it, you see the shape of the Warden's weakness.")
                player.luck += 2
                story("Your luck increases by 2. The mirror cracks and goes dark.")
                current_room.interactables = [obj for obj in current_room.interactables if obj.name != "Black Mirror"]
                continue

            if lower_name in {"ash altar", "altar"}:
                heart = player.inventory.has_item("Warden's Heart")
                if heart is None:
                    story("The altar is empty. It is waiting for a heart made of ash and iron.")
                else:
                    player.inventory.remove_item(heart)
                    player.max_health += 20
                    player.health = player.max_health
                    story("You place the Warden's Heart into the altar. The dungeon shudders, and your body is remade stronger.")
                    story("Your maximum health increases by 20.")
                continue

            if lower_name == "shrine":
                story("You kneel before the shrine. The candles flicker and a cold wave of calm passes through you.")
                recovery = min(12, player.max_health - player.health)
                if recovery > 0:
                    player.health += recovery
                    story(f"Your wounds soothe themselves and you recover {recovery} health.")
                else:
                    story("The shrine offers no more comfort; you are already whole.")
                continue

            if lower_name == "forge":
                story("You warm your hands near the forge and listen to the old metal speak. It feels like memory in the stone.")
                if player.weapon is not None:
                    story(f"Your {player.weapon.name} glows faintly under the forge's heat.")
                else:
                    story("There is no weapon in your hands, but the forge still breathes with heat.")
                continue

            story(f"You try to use the {target_name}, but it does nothing useful.")
            continue

        if command.startswith("combine "):
            recipe_text = command[8:].strip()
            if " with " in recipe_text:
                first_name, second_name = recipe_text.split(" with ", 1)
            else:
                parts = recipe_text.split()
                if len(parts) < 2:
                    story("Combine which two items?")
                    continue
                first_name = parts[0]
                second_name = " ".join(parts[1:])

            first_item = player.inventory.has_item(first_name.strip())
            second_item = player.inventory.has_item(second_name.strip())
            player.combine_items(first_item, second_item)
            continue

        if command.startswith("drop "):
            item_name = command[5:].strip()
            item = player.inventory.has_item(item_name)
            if item is None:
                story(f"You do not have {item_name}.")
            else:
                player.drop_item(item, current_room)
            continue

        if command.startswith("fight") or command == "attack":
            if not current_room.enemy:
                story("There is no enemy here to fight.")
                continue

            enemy = current_room.enemy[0]
            battle = BattleEngine(player, enemy)
            battle.run()

            if enemy.health <= 0:
                current_room.enemy = []
                current_room.cleared = True
                for item in enemy.inventory:
                    current_room.add_item(item)
                story(f"The {enemy.name} falls. The room is now cleared.")
                if enemy.is_boss:
                    ending(player)
                    running = False
            continue

        if command in {"map", "rooms"}:
            story("Known rooms:")
            for room in rooms:
                status = "cleared" if room.cleared else "unsafe"
                locked_text = " locked" if room.locked else " open"
                story(f"- {room.name} ({status}{locked_text})")
            continue

        story("You hesitate. The dungeon does not understand that command.")

    if player.health <= 0:
        story("The story closes on your final breath.")


if __name__ == "__main__":
    main()