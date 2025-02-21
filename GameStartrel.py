import time
import random
import json
import os

class Player:
    def __init__(self, hp=100, defense=0, attack=0, coins=100, inventory=None, zone=1, 
                 armor_enchant="", weapon_enchant="", daily_streak=0, last_daily=0, 
                 level=0, xp=0, equipped_weapon=None, equipped_armor=None, 
                 cleared_zones=None):
        if inventory is None:
            inventory = {
                "fish": 0, "golden_fish": 0, "wood": 0, "epic_wood": 0, 
                "apple": 0, "banana": 0, "zone_1_key": 0, "zone_2_key": 0, 
                "zone_3_key": 0, "evil_ray": 0, "hell_orb": 0, "zombie_hand": 0,
                "rune_of_gods_1": 0, "rune_of_gods_2": 0, "ruby": 0,
                "evil_mask": 0, "hell_armor": 0
            }
        if cleared_zones is None:
            cleared_zones = set([1])  # Множество пройденных зон
        
        self.hp = hp
        self.max_hp = 100 + (level * 5)
        self.defense = defense
        self.attack = attack
        self.coins = coins
        self.inventory = inventory
        self.zone = zone
        self.cleared_zones = cleared_zones
        self.armor_enchant = armor_enchant
        self.weapon_enchant = weapon_enchant
        self.daily_streak = daily_streak
        self.last_daily = last_daily
        self.level = level
        self.xp = xp
        self.xp_to_next = self.calculate_next_level_xp()
        self.equipped_weapon = equipped_weapon  # "evil_ray" или "hell_orb"
        self.equipped_armor = equipped_armor    # "evil_mask" или "hell_armor"

    def equip_item(self, item):
        if item in ["evil_ray", "hell_orb"]:
            old_attack = self.attack
            if self.equipped_weapon:
                # Снимаем эффекты старого оружия
                if self.equipped_weapon == "evil_ray":
                    self.attack -= 50
                elif self.equipped_weapon == "hell_orb":
                    self.attack -= 35
            self.equipped_weapon = item
            self.attack = old_attack + (50 if item == "evil_ray" else 35)
            print(f"Оружие {item} экипировано!")
        
        elif item in ["evil_mask", "hell_armor"]:
            old_defense = self.defense
            if self.equipped_armor:
                # Снимаем эффекты старой брони
                if self.equipped_armor == "evil_mask":
                    self.defense -= 25
                elif self.equipped_armor == "hell_armor":
                    self.defense -= 40
            self.equipped_armor = item
            self.defense = old_defense + (25 if item == "evil_mask" else 40)
            print(f"Броня {item} экипирована!")

    def switch_zone(self, target_zone):
        if target_zone > max(self.cleared_zones):
            print("Вы не можете переключиться на следующую зону.")
            return False
        self.zone = target_zone
        print(f"Вы переключились на зону {self.zone}")
        return True
            
        def calculate_next_level_xp(self):
            if self.level == 0:
                return 100
            return int(self.xp_to_next * (1 + 15/100))  # Using 15% growth rate

    def add_xp(self, amount):
        self.xp += amount
        print(f"+{amount} XP!")
        
        while self.xp >= self.xp_to_next:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.xp -= self.xp_to_next
        self.xp_to_next = self.calculate_next_level_xp()
        
        # Apply level-up bonuses
        self.max_hp += 5
        self.hp = self.max_hp  # Heal to full on level up
        self.attack += 0.5
        self.defense += 0.5
        
        print(f"\nУровень повышен! Текущий уровень: {self.level}")
        print(f"Бонусы уровня:")
        print(f"+5 к максимальному HP (Всего: {self.max_hp})")
        print(f"+0.5 к атаке (Всего: {self.attack})")
        print(f"+0.5 к защите (Всего: {self.defense})")
        print(f"До следующего уровня требуется {self.xp_to_next} XP\n")

    def mine(self):
        if self.zone < 3:
            print("Майнинг доступен только с 3 зоны!")
            return
            
        if random.random() < 0.85:  # 85% шанс получить монеты
            coins_reward = random.randint(1000, 1500)
            self.coins += coins_reward
            print(f"Вы намайнили {coins_reward} монет!")
        else:  # 15% шанс получить рубин
            self.inventory["ruby"] += 1
            print("Вы намайнили рубин!")

    def daily(self):
        current_time = time.time()
        time_since_last = current_time - self.last_daily
        
        if time_since_last < 86400:  # 24 часа
            hours_remaining = int((86400 - time_since_last) / 3600)
            minutes_remaining = int(((86400 - time_since_last) % 3600) / 60)
            print(f"Daily будет доступен через {hours_remaining} часов и {minutes_remaining} минут")
            return
            
        # Проверяем, прошло ли больше 48 часов с последнего daily
        if time_since_last > 172800:  # 48 часов
            self.daily_streak = 0
            
        # Обновляем время последнего daily
        self.last_daily = current_time
        
        # Увеличиваем стрик
        self.daily_streak = min(self.daily_streak + 1, 7)
        
        # Базовая награда
        base_coins = 350 * (1.75 ** (self.zone - 1))
        
        # Бонус за стрик
        streak_bonus = base_coins * (self.daily_streak * 0.1)
        total_coins = int(base_coins + streak_bonus)
        
        self.coins += total_coins
        self.hp = min(self.hp + 50, self.max_hp)
        
        print(f"Daily награда получена!")
        print(f"+ {total_coins} монет")
        print(f"+ 50 HP")
        print(f"Текущий стрик: {self.daily_streak}")
        
        # Шанс получить Руну Божества №2 на 7-ом стрике
        if self.daily_streak == 7 and random.random() < 0.05:
            self.inventory["rune_of_gods_2"] += 1
            if self.inventory["rune_of_gods_2"] == 1:
                print("\nЧто... это? Я вижу такое впервые... Если я не ошибаюсь, то пророчество говорило что если собрать 8 подобных рун и один странный элемент который был порван в пергаменте и неизвестно где находится, и собрать их в машину Хроноса то этим можно что то сделать... Но пусть пока что у меня останется...")
            else:
                print("\nВот и еще одна... С таким темпом думаю я смогу собрать руны довольно таки быстро...")

    def enchant(self, item_type):
        enchants = {
            "Fine": (0.4, 1.1),
            "Mediocre": (0.3, 1.2),
            "Worthy": (0.25, 1.35),
            "Exquisite": (0.15, 1.5),
            "Great": (0.1, 1.6),
            "Legendary": (0.05, 1.75),
            "Masterful": (0.025, 1.9),
            "Absolute": (0.01, 2.1),
            "Divine": (0.005, 2.5),
            "ETERNAL": (0.001, 3.0)
        }

        base_cost = 750
        zone_multiplier = 1 + (0.1 * (self.zone - 2))
        cost = int(base_cost * zone_multiplier)

        if self.zone < 2:
            print("Зачарование доступно только со 2 зоны!")
            return
        
        if self.coins < cost:
            print("У вас недостаточно монет!")
            return

        self.coins -= cost
        
        roll = random.random()
        cumulative_prob = 0
        selected_enchant = None
        
        for enchant, (prob, multiplier) in enchants.items():
            cumulative_prob += prob
            if roll <= cumulative_prob:
                selected_enchant = (enchant, multiplier)
                break

        if item_type == "armor":
            old_enchant = self.armor_enchant
            self.armor_enchant = selected_enchant[0]
            base_defense = self.defense / (enchants[old_enchant][1] if old_enchant else 1)
            self.defense = int(base_defense * selected_enchant[1])
        else:  # weapon
            old_enchant = self.weapon_enchant
            self.weapon_enchant = selected_enchant[0]
            base_attack = self.attack / (enchants[old_enchant][1] if old_enchant else 1)
            self.attack = int(base_attack * selected_enchant[1])

        print(f"Получено зачарование: {selected_enchant[0]}!")

    def buy_item(self, item):
        if item == "sword" and self.coins >= 40:
            self.attack += 1
            self.coins -= 40
            print("Вы купили начальный меч.")
        elif item == "armor" and self.coins >= 50:
            self.defense += 2
            self.coins -= 50
            print("Вы купили начальную броню.")
        elif item == "3" and self.coins >= 10:
            heal_amount = min(45, self.max_hp - self.hp)  # Изменено лечение
            self.hp += heal_amount
            self.coins -= 10
            print(f"Вы купили зелье лечения и восстановили {heal_amount} HP.")
        elif item == "zone1_key" and self.coins >= 1000:
            self.inventory["zone_1_key"] += 1
            self.coins -= 1000
            print("Вы купили ключ к данжу первой зоны.")
        elif item == "zone2_key" and self.coins >= 5000:
            self.inventory["zone_2_key"] += 1
            self.coins -= 5000
            print("Вы купили ключ к данжу второй зоны.")
        elif item == "zone3_key" and self.coins >= 10000:
            self.inventory["zone_3_key"] += 1
            self.coins -= 10000
            print("Вы купили ключ к данжу третьей зоны.")
        else:
            print("Недостаточно монет или неверный предмет.")

    def take_damage(self, damage):
        reduced_damage = max(0, damage - self.defense)
        self.hp -= reduced_damage
        print(f"Вы получили {reduced_damage} урона. Осталось {self.hp} HP.")
        if self.hp <= 0:
            self.die()

# Modify the die method in the Player class
def die(self):
    # Calculate coin loss based on zone
    base_loss = 100
    zone_multiplier = 1 + (0.25 * (self.zone - 1))  # +25% per zone
    loss = min(int(base_loss * zone_multiplier), self.coins)
    
    # Don't lose coins if player has coin armor
    if not hasattr(self, 'has_coin_armor') or not self.has_coin_armor:
        self.coins -= loss
        print(f"Вы потеряли {loss} монет.")
    
    # Level loss for players level 5+
    if self.level >= 5:
        self.level -= 1
        print(f"Вы потеряли уровень! Текущий уровень: {self.level}")
        
    self.hp = self.max_hp
    print(f"Осталось монет: {self.coins}")

    def hunt(self):
        monsters = {
            1: {
                "names": ["Slime", "Zombie", "Skeleton"],
                "hp": 5,
                "damage": (4, 7),
                "coins": (10, 34),
                "xp": (20, 55),  # Added XP range
                "special_drops": {
                    "Zombie": ("zombie_hand", 0.03, 4)
                }
            },
            2: {
                "names": ["Stray", "Soldier", "Schism"],
                "hp": 15,
                "damage": (16, 24),
                "coins": (78, 120),
                "xp": (99, 170),  # Added XP range
                "special_drops": {
                    "Soldier": ("coins_bonus", 0.50, 1.75)
                }
            },
            3: {
                "names": ["Stalker", "Drone", "Sentry"],
                "hp": 24,
                "damage": (30, 49),
                "coins": (349, 420),
                "xp": (320, 470),  # Added XP range
                "special_drops": {
                    "Stalker": ("rune_of_gods_1", 0.06)
                }
            }
        }
        
        zone_data = monsters[self.zone]
        monster_name = random.choice(zone_data["names"])
        monster_hp = zone_data["hp"]
        print(f"Вы встретили монстра: {monster_name}")
        
        while monster_hp > 0 and self.hp > 0:
            damage_dealt = self.attack
            if "zombie_hand" in self.inventory and self.inventory["zombie_hand"] > 0:
                damage_dealt += 4
            else:
                damage_dealt += 2
            
            monster_hp -= damage_dealt
            print(f"Вы нанесли {damage_dealt} урона монстру. У монстра осталось {max(0, monster_hp)} HP")
            
            if monster_hp <= 0:
                base_reward = random.randint(zone_data["coins"][0], zone_data["coins"][1])
                xp_reward = random.randint(zone_data["xp"][0], zone_data["xp"][1])  # Added XP reward
                reward = base_reward
                
                if monster_name == "Soldier" and random.random() < 0.50:
                    reward = int(base_reward * 1.75)
                    print("Soldier dropped extra coins!")
                
                self.coins += reward
                self.add_xp(xp_reward)  # Add XP to player
                print(f"Монстр побежден! +{reward} монет.")
                
                if monster_name in zone_data["special_drops"]:
                    drop_data = zone_data["special_drops"][monster_name]
                    if random.random() < drop_data[1]:
                        if drop_data[0] == "zombie_hand":
                            self.inventory["zombie_hand"] += 1
                            print("Вам выпал редкий предмет: Рука зомби!")
                        elif drop_data[0] == "rune_of_gods_1":
                            self.inventory["rune_of_gods_1"] += 1
                            if self.inventory["rune_of_gods_1"] == 1:
                                print("\nЧто... это? Я вижу такое впервые...")
                            else:
                                print("\nВот и еще одна...")
                break
                
            damage = random.randint(zone_data["damage"][0], zone_data["damage"][1])
            damage_taken = max(0, damage - self.defense)
            self.hp -= damage_taken
            print(f"Получено урона: {damage_taken}. Осталось HP: {self.hp}")
            
            if self.hp <= 0:
                self.die()
                break

    def view_recipes(self):
        print("=== ДОСТУПНЫЕ РЕЦЕПТЫ ===")
        print("\nБАЗОВЫЕ РЕЦЕПТЫ:")
        print("Рыбный меч: 15 дерева, 1 эпическое дерево (+3 урона)")
        print("Рыбная броня: 30 дерева, 2 эпического дерева (+3.5 защиты)")
        
        if self.level >= 3:
            print("\nРЕЦЕПТЫ 3+ УРОВНЯ:")
            print("Рыбный меч: 15 рыб, 1 золотая рыба (+4 урона)")
            print("Рыбная броня: 20 рыб, 2 золотой рыбы (+4.5 защиты)")
        
        if self.level >= 5:
            print("\nРЕЦЕПТЫ 5+ УРОВНЯ:")
            print("Яблочный меч: 25 яблок, 1 банан (+5.5 урона)")
            print("Яблочная броня: 40 яблок, 1 банан (+6 защиты)")
            print("Амулет жизни: 1750 монет, 50 яблок, 2 эпического дерева (+50 жизней)")
        
        if self.level >= 7:
            print("\nРЕЦЕПТЫ 7+ УРОВНЯ:")
            print("Бананаранг: 8 бананов (+8.5 урона, 30% шанс снять 40% HP с монстра)")
            print("Банановый щит: 6 бананов (+7 защиты)")
        
        if self.level >= 10:
            print("\nРЕЦЕПТЫ 10+ УРОВНЯ:")
            print("Монетный меч: 12345 монет, 6 эпического дерева, 1 золотая рыба")
            print("(+16 урона, 70% шанс 1.5x монет, 30% шанс 2x монет)")
            print("Монетная броня: 12345 монет, 8 эпического дерева, 2 золотой рыбы")
            print("(+17 защиты, защита от потери монет при смерти)")

def craft_recipe(player, item):
    if item == "fish_sword_basic":
        if player.inventory["wood"] >= 15 and player.inventory["epic_wood"] >= 1:
            player.inventory["wood"] -= 15
            player.inventory["epic_wood"] -= 1
            player.attack += 3
            print("Рыбный меч создан! (+3 урона)")
            return True
            
    elif item == "fish_armor_basic":
        if player.inventory["wood"] >= 30 and player.inventory["epic_wood"] >= 2:
            player.inventory["wood"] -= 30
            player.inventory["epic_wood"] -= 2
            player.defense += 3.5
            print("Рыбная броня создана! (+3.5 защиты)")
            return True
            
    elif item == "fish_sword" and player.level >= 3:
        if player.inventory["fish"] >= 15 and player.inventory["golden_fish"] >= 1:
            player.inventory["fish"] -= 15
            player.inventory["golden_fish"] -= 1
            player.attack += 4
            print("Рыбный меч создан! (+4 урона)")
            return True
            
    elif item == "fish_armor" and player.level >= 3:
        if player.inventory["fish"] >= 20 and player.inventory["golden_fish"] >= 2:
            player.inventory["fish"] -= 20
            player.inventory["golden_fish"] -= 2
            player.defense += 4.5
            print("Рыбная броня создана! (+4.5 защиты)")
            return True
            
    elif item == "apple_sword" and player.level >= 5:
        if player.inventory["apple"] >= 25 and player.inventory["banana"] >= 1:
            player.inventory["apple"] -= 25
            player.inventory["banana"] -= 1
            player.attack += 5.5
            print("Яблочный меч создан! (+5.5 урона)")
            return True
            
    elif item == "apple_armor" and player.level >= 5:
        if player.inventory["apple"] >= 40 and player.inventory["banana"] >= 1:
            player.inventory["apple"] -= 40
            player.inventory["banana"] -= 1
            player.defense += 6
            print("Яблочная броня создана! (+6 защиты)")
            return True
            
    elif item == "life_amulet" and player.level >= 5:
        if player.coins >= 1750 and player.inventory["apple"] >= 50 and player.inventory["epic_wood"] >= 2:
            player.coins -= 1750
            player.inventory["apple"] -= 50
            player.inventory["epic_wood"] -= 2
            player.max_hp += 50
            player.hp = player.max_hp
            print("Амулет жизни создан! (+50 максимального здоровья)")
            return True
            
    elif item == "bananarang" and player.level >= 7:
        if player.inventory["banana"] >= 8:
            player.inventory["banana"] -= 8
            player.attack += 8.5
            print("Бананаранг создан! (+8.5 урона, 30% шанс снять 40% HP с монстра)")
            return True
            
    elif item == "banana_shield" and player.level >= 7:
        if player.inventory["banana"] >= 6:
            player.inventory["banana"] -= 6
            player.defense += 7
            print("Банановый щит создан! (+7 защиты)")
            return True
            
    elif item == "coin_sword" and player.level >= 10:
        if (player.coins >= 12345 and player.inventory["epic_wood"] >= 6 
                and player.inventory["golden_fish"] >= 1):
            player.coins -= 12345
            player.inventory["epic_wood"] -= 6
            player.inventory["golden_fish"] -= 1
            player.attack += 16
            print("Монетный меч создан! (+16 урона)")
            return True
            
    elif item == "coin_armor" and player.level >= 10:
        if (player.coins >= 12345 and player.inventory["epic_wood"] >= 8 
                and player.inventory["golden_fish"] >= 2):
            player.coins -= 12345
            player.inventory["epic_wood"] -= 8
            player.inventory["golden_fish"] -= 2
            player.defense += 17
            print("Монетная броня создана! (+17 защиты)")
            return True
            
    print("Недостаточно ресурсов или уровня для крафта!")
    return False

    def fish(self, command):
        if self.zone >= 2 and command == "net":
            fish_count = int(random.randint(2, 5) * 1.75)
            golden_fish_chance = 0.1 * 1.5
        else:
            fish_count = random.randint(2, 5)
            golden_fish_chance = 0.1
            
        golden_fish = random.random() < golden_fish_chance
        self.inventory["fish"] += fish_count
        print(f"Вы поймали {fish_count} рыбы.")
        if golden_fish:
            self.inventory["golden_fish"] += 1
            print("Вы поймали золотую рыбку!")

    def chop_tree(self, command):
        if self.zone >= 2 and command == "axe":
            wood_count = int(random.randint(3, 7) * 1.75)
            epic_wood_chance = 0.1 * 1.5
        else:
            wood_count = random.randint(3, 7)
            epic_wood_chance = 0.1
            
        epic_wood = random.random() < epic_wood_chance
        self.inventory["wood"] += wood_count
        print(f"Вы срубили дерево и получили {wood_count} древесины.")
        if epic_wood:
            self.inventory["epic_wood"] += 1
            print("Вы получили эпическое дерево!")

    def collect(self, command):
        if self.zone >= 2 and command == "ladder":
            apple_count = int(random.randint(1, 3) * 1.75)
            banana_chance = 0.1 * 1.5
        else:
            apple_count = random.randint(1, 3)
            banana_chance = 0.1
            
        banana_count = 1 if random.random() < banana_chance else 0
        self.inventory["apple"] += apple_count
        self.inventory["banana"] += banana_count
        print(f"Вы собрали {apple_count} яблок.")
        if banana_count > 0:
            print("Вы нашли банан!")

def show_profile(self):
        print(f"Профиль игрока:")
        print(f"Уровень: {self.level}")
        print(f"XP: {self.xp}/{self.xp_to_next}")
        print(f"HP: {self.hp}/{self.max_hp}")
        print(f"Атака: {self.attack}")
        print(f"Защита: {self.defense}")
        print(f"Монеты: {self.coins}")
        print(f"Текущая зона: {self.zone}")
        print(f"Пройденные зоны: {sorted(list(self.cleared_zones))}")
        print(f"Экипированное оружие: {self.equipped_weapon or 'Нет'}")
        print(f"Экипированная броня: {self.equipped_armor or 'Нет'}")

    def show_inventory(self):
        print(f"Инвентарь:\нРыба: {self.inventory.get('fish', 0)}\нЗолотая рыба: {self.inventory.get('golden_fish', 0)}\нДревесина: {self.inventory.get('wood', 0)}\нЭпическое дерево: {self.inventory.get('epic_wood', 0)}\нЯблоки: {self.inventory.get('apple', 0)}\нБананы: {self.inventory.get('banana', 0)}")

def trade(self, item, quantity=1):
    if item == "1" and self.inventory["fish"] >= quantity:
        self.inventory["fish"] -= quantity
        self.inventory["wood"] += 2 * quantity
        print(f"Вы обменяли {quantity} рыбу на {2 * quantity} древесины.")
    elif item == "2" and self.inventory["wood"] >= 2 * quantity:
        self.inventory["wood"] -= 2 * quantity
        self.inventory["fish"] += quantity
        print(f"Вы обменяли {2 * quantity} древесины на {quantity} рыбу.")
    elif item == "3" and self.inventory["wood"] >= 6 * quantity:
        self.inventory["wood"] -= 6 * quantity
        self.inventory["apple"] += quantity
        print(f"Вы обменяли {6 * quantity} древесины на {quantity} яблок.")
    elif item == "4" and self.inventory["fish"] >= 3 * quantity:
        self.inventory["fish"] -= 3 * quantity
        self.inventory["apple"] += quantity
        print(f"Вы обменяли {3 * quantity} рыбы на {quantity} яблок.")
    elif item == "5" and self.inventory["apple"] >= quantity:
        self.inventory["apple"] -= quantity
        self.inventory["wood"] += 6 * quantity
        print(f"Вы обменяли {quantity} яблок на {6 * quantity} древесины.")
    elif item == "6" and self.inventory["apple"] >= quantity:
        self.inventory["apple"] -= quantity
        self.inventory["fish"] += 3 * quantity
        print(f"Вы обменяли {quantity} яблок на {3 * quantity} рыбы.")
    elif item == "7" and self.inventory["ruby"] >= quantity:
        self.inventory["ruby"] -= quantity
        self.inventory["wood"] += 350 * quantity
        print(f"Вы обменяли {quantity} рубин на {350 * quantity} древесины.")
    elif item == "8" and self.inventory["ruby"] >= quantity:
        self.inventory["ruby"] -= quantity
        self.inventory["fish"] += 175 * quantity
        print(f"Вы обменяли {quantity} рубин на {175 * quantity} рыбы.")
    else:
        print("Недостаточно ресурсов для обмена.")

    def sell(self, item, quantity=1):
        if item == "fish" and self.inventory["fish"] >= quantity:
            self.coins += 20 * quantity
            self.inventory["fish"] -= quantity
            print(f"Вы продали {quantity} рыбу за {20 * quantity} монет.")
        elif item == "golden_fish" and self.inventory["golden_fish"] >= quantity:
            self.coins += 200 * quantity
            self.inventory["golden_fish"] -= quantity
            print(f"Вы продали {quantity} золотую рыбу за {200 * quantity} монет.")
        elif item == "wood" and self.inventory["wood"] >= quantity:
            self.coins += 10 * quantity
            self.inventory["wood"] -= quantity
            print(f"Вы продали {quantity} древесины за {10 * quantity} монет.")
        elif item == "epic_wood" and self.inventory["epic_wood"] >= quantity:
            self.coins += 150 * quantity
            self.inventory["epic_wood"] -= quantity
            print(f"Вы продали {quantity} эпическое дерево за {150 * quantity} монет.")
        elif item == "apple" and self.inventory["apple"] >= quantity:
            self.coins += 50 * quantity
            self.inventory["apple"] -= quantity
            print(f"Вы продали {quantity} яблок за {50 * quantity} монет.")
        elif item == "banana" and self.inventory["banana"] >= quantity:
            self.coins += 300 * quantity
            self.inventory["banana"] -= quantity
            print(f"Вы продали {quantity} банан за {300 * quantity} монет.")
        elif item == "ruby" and self.inventory["ruby"] >= quantity:
            self.coins += 3500 * quantity
            self.inventory["ruby"] -= quantity
            print(f"Вы продали {quantity} рубин за {3500 * quantity} монет.")
        else:
            print("Недостаточно ресурсов для продажи.")

    def craft(self, item, quantity=1):
        if item == "golden_fish" and self.inventory["fish"] >= 15 * quantity:
            self.inventory["fish"] -= 15 * quantity
            self.inventory["golden_fish"] += quantity
            print(f"Вы скрафтили {quantity} золотую рыбу.")
        elif item == "epic_wood" and self.inventory["wood"] >= 15 * quantity:
            self.inventory["wood"] -= 15 * quantity
            self.inventory["epic_wood"] += quantity
            print(f"Вы скрафтили {quantity} эпическое дерево.")
        elif item == "banana" and self.inventory["apple"] >= 6 * quantity:
            self.inventory["apple"] -= 6 * quantity
            self.inventory["banana"] += quantity
            print(f"Вы скрафтили {quantity} банан.")
        else:
            print("Недостаточно ресурсов для крафта.")

    def dismantle(self, item, quantity=1):
        if item == "golden_fish" and self.inventory["golden_fish"] >= quantity:
            self.inventory["golden_fish"] -= quantity
            self.inventory["fish"] += int(15 * 0.75 * quantity)
            print(f"Вы разобрали {quantity} золотую рыбу и получили {int(15 * 0.75 * quantity)} рыбы.")
        elif item == "epic_wood" and self.inventory["epic_wood"] >= quantity:
            self.inventory["epic_wood"] -= quantity
            self.inventory["wood"] += int(15 * 0.75 * quantity)
            print(f"Вы разобрали {quantity} эпическое дерево и получили {int(15 * 0.75 * quantity)} древесины.")
        elif item == "banana" and self.inventory["banana"] >= quantity:
            self.inventory["banana"] -= quantity
            self.inventory["apple"] += int(6 * 0.75 * quantity)
            print(f"Вы разобрали {quantity} банан и получили {int(6 * 0.75 * quantity)} яблок.")
        else:
            print("Недостаточно ресурсов для разборки.")

def dungeon(self):
    key_names = {1: "zone_1_key", 2: "zone_2_key", 3: "zone_3_key"}
    key_name = key_names[self.zone]
    
    if self.inventory[key_name] < 1:
        print("У вас нет ключа для входа в данж!")
        return

    self.inventory[key_name] -= 1
    print(f"Вы входите в данж зоны {self.zone}...")

    bosses = {
        1: [
            {"name": "Зловещее лицо", "hp": 50, "damage": 40, 
             "reward": (1700, 2200), "drop": "evil_ray", "drop_chance": 0.01,
             "special_drop": "evil_mask", "special_chance": 0.05},
            {"name": "Цербер", "hp": 50, "damage": 40,
             "reward": (1700, 2200), "drop": "hell_orb", "drop_chance": 0.01,
             "special_drop": "hell_armor", "special_chance": 0.05}
        ],
        2: [
            {"name": "Отвратная масса", "hp": 100, "damage": 80,
             "reward": (3440, 4770), "drop": None, "drop_chance": 0},
            {"name": "Меч машина", "hp": 150, "damage": 95,
             "reward": (6770, 7800), "drop": None, "drop_chance": 0}
        ]
    }

    for boss in bosses[self.zone]:
        if boss["name"] == "Меч машина" and random.random() > 0.1:
            continue

        boss_hp = boss["hp"]
        print(f"\nПоявляется босс: {boss['name']} (HP: {boss_hp})")

        while boss_hp > 0 and self.hp > 0:
            damage_to_boss = 2 + (self.attack * 2)
            boss_hp -= damage_to_boss
            print(f"Вы нанесли {damage_to_boss} урона боссу. У босса осталось {max(0, boss_hp)} HP")

            if boss_hp <= 0:
                reward = random.randint(boss["reward"][0], boss["reward"][1])
                self.coins += reward
                print(f"Вы победили {boss['name']} и получили {reward} монет!")
                
                # Обычный дроп
                if boss["drop"] and random.random() < boss["drop_chance"]:
                    self.inventory[boss["drop"]] += 1
                    self.equip_item(boss["drop"])
                    print(f"Вы получили редкий предмет: {boss['drop']}!")
                
                # Специальный дроп (броня)
                if boss["special_drop"] and random.random() < boss["special_chance"]:
                    self.inventory[boss["special_drop"]] += 1
                    self.equip_item(boss["special_drop"])
                    print(f"Вы получили редкий предмет: {boss['special_drop']}!")
                
                break

            # Урон от босса с учетом эффектов предметов
            damage_to_player = boss["damage"] * (1 - (self.defense * 0.02))
            self.take_damage(damage_to_player)
            
            # Эффекты предметов
            if self.equipped_weapon == "hell_orb" and random.random() < 0.3:
                heal = 15
                self.hp = min(self.hp + heal, self.max_hp)
                print(f"Hell Orb исцеляет вас на {heal} HP!")
            
            if self.equipped_armor == "evil_mask" and random.random() < 0.45:
                heal = 10
                self.hp = min(self.hp + heal, self.max_hp)
                print(f"Зловещая маска исцеляет вас на {heal} HP!")
            
            if self.hp <= 0:
                print(f"Вы погибли в битве с {boss['name']}!")
                return

        if self.hp > 0 and self.zone not in self.cleared_zones:
            self.cleared_zones.add(self.zone)
            if self.zone < 3:
                self.zone += 1
                self.cleared_zones.add(self.zone)
                print(f"Поздравляем! Вы прошли данж и перешли в зону {self.zone}!")

def save_progress(player):
    with open("savegame.json", "w") as file:
        data = player.__dict__.copy()
        data['cleared_zones'] = list(player.cleared_zones)  # Преобразуем set в list для JSON
        json.dump(data, file)
    print("Прогресс сохранен.")

def load_progress():
    if os.path.exists("savegame.json"):
        with open("savegame.json", "r") as file:
            data = json.load(file)
            data['cleared_zones'] = set(data.get('cleared_zones', [1]))  # Преобразуем list обратно в set
            return Player(
                hp=data.get("hp", 100),
                defense=data.get("defense", 0),
                attack=data.get("attack", 0),
                coins=data.get("coins", 100),
                inventory=data.get("inventory", None),
                zone=data.get("zone", 1),
                armor_enchant=data.get("armor_enchant", ""),
                weapon_enchant=data.get("weapon_enchant", ""),
                daily_streak=data.get("daily_streak", 0),
                last_daily=data.get("last_daily", 0),
                level=data.get("level", 0),
                xp=data.get("xp", 0),
                equipped_weapon=data.get("equipped_weapon", None),
                equipped_armor=data.get("equipped_armor", None),
                cleared_zones=data.get("cleared_zones", set([1]))
            )
    return Player()

def shop(player):
    items_for_sale = {
        "1": ("zone_1_key", 1000),
        "2": ("zone_2_key", 10000),
        "3": ("zone_3_key", 25000),
        "4": ("sword", 40),
        "5": ("armor", 50),
        "6": ("healing_potion", 300)
    }

    print("Добро пожаловать в магазин! Вот что у нас есть:")
    for num, (item, base_price) in items_for_sale.items():
        if item.startswith("zone_"):
            zone_num = int(item.split('_')[1])
            # Показываем ключ только для текущей зоны или уже пройденных со скидкой
            if zone_num > player.zone and zone_num not in player.cleared_zones:
                continue
            price = int(base_price * 0.65) if zone_num in player.cleared_zones else base_price
        else:
            price = base_price
        
        print(f"{num}. {item}: {price} монет")

    choice = input("Что вы хотите купить? Введите номер предмета: ").strip()
    if choice in items_for_sale:
        item, base_price = items_for_sale[choice]
        price = int(base_price * 0.65) if (item.startswith("zone_") and int(item.split('_')[1]) in player.cleared_zones) else base_price
        
        if player.coins >= price:
            if item == "sword":
                player.attack += 1
                player.coins -= price
                print(f"Вы купили {item} за {price} монет.")
            elif item == "armor":
                player.defense += 2
                player.coins -= price
                print(f"Вы купили {item} за {price} монет.")
            else:
                player.coins -= price
                player.inventory[item] = player.inventory.get(item, 0) + 1
                print(f"Вы купили {item} за {price} монет.")
        else:
            print("У вас недостаточно монет для покупки этого предмета.")
    else:
        print("Такого предмета нет в магазине.")

def is_first_time():
    return not os.path.exists("savegame.json")

def show_first_time_welcome():
    print("Здравствуй путник!")
    time.sleep(1)
    print("Добро пожаловать в наш RPG мир! Здесь ты можешь выживать, развиваться а также сражаться с множество монстрами и боссами.")
    time.sleep(2)
    print("Ох, что-то я затянулся. Ладно, дальше уже сам разберешься, ведь эта игра легкая! Удачи тебе!")
    print("---")

def main():
    if is_first_time():
        show_first_time_welcome()
        
    elif command.startswith("cd") or command.startswith("cooldown"):
    parts = command.split()
    if len(parts) == 1:
        for action, cooldown in cooldowns.items():
            remaining = max(0, int(cooldown - current_time))
            if remaining == 0:
                print(f"Команда '{action}' готова.")
            else:
                print(f"Команда '{action}' будет доступна через {remaining} секунд.")
    elif len(parts) == 2 and parts[1].startswith("switch"):
        try:
            zone_num = int(parts[1].split()[1])
            player.switch_zone(zone_num)
        except (IndexError, ValueError):
            print("Используйте: cd switch 1/2/3")
    print()
    
    else:
        print("Добро пожаловать!")
    
    player = load_progress()
    cooldowns = {
        "hunt": 0,
        "fish": 0,
        "chop": 0,
        "collect": 0,
        "dungeon": 0,
        "mine": 0
    }

    commands = {
        "help": "Показать список команд",
        "shop": "Открыть магазин",
        "profile (p)": "Показать профиль игрока",
        "inventory (i)": "Показать инвентарь",
        "hunt": "Охотиться на монстров (кулдаун 30 секунд)",
        "fish": "Рыбачить (кулдаун 1 минута 30 секунд)",
        "chop": "Срубить дерево (кулдаун 1 минута 30 секунд)",
        "collect": "Собирать яблоки и бананы (кулдаун 1 минута)",
        "mine": "Майнить руду (кулдаун 20 минут, доступно с 3 зоны)",
        "daily": "Получить ежедневную награду (кулдаун 24 часа)",
        "cd (cooldown)": "Показать оставшееся время кулдауна команд",
        "trade": "Обменять ресурсы",
        "sell": "Продать ресурсы",
        "craft": "Скрафтить предмет",
        "dismantle": "Разобрать предмет",
        "dungeon (dung)": "Войти в данж текущей зоны",
        "enchant": "Зачаровать меч или броню (доступно со 2 зоны)",
        "-": "Команды для сохранения и выхода",
        "save": "Сохранить прогресс",
        "exit": "Выйти из игры"
    }

    zone_2_commands = {
        "net": "Улучшенная рыбалка (1.75x рыбы, 1.5x шанс золотой рыбы)",
        "axe": "Улучшенная срубка (1.75x дерева, 1.5x шанс эпического дерева)",
        "ladder": "Улучшенный сбор (1.75x яблок, 1.5x шанс банана)"
    }

    print("Добро пожаловать в игру!")
    time.sleep(2)
    print("Список команд:")
    for cmd, desc in commands.items():
        print(f"{cmd}: {desc}")
    print()

player = load_progress()
cooldowns = {
    "hunt": 0,
    "fish": 0,
    "chop": 0,
    "collect": 0,
    "dungeon": 0,
    "mine": 0
}
commands = {
    "help": "Показать список команд",
    "shop": "Открыть магазин",
    "profile (p)": "Показать профиль игрока",
    "inventory (i)": "Показать инвентарь",
    "hunt": "Охотиться на монстров (кулдаун 30 секунд)",
    "fish": "Рыбачить (кулдаун 1 минута 30 секунд)",
    "chop": "Срубить дерево (кулдаун 1 минута 30 секунд)",
    "collect": "Собирать яблоки и бананы (кулдаун 1 минута)",
    "mine": "Майнить руду (кулдаун 20 минут, доступно с 3 зоны)",
    "daily": "Получить ежедневную награду (кулдаун 24 часа)",
    "cd (cooldown)": "Показать оставшееся время кулдауна команд",
    "trade": "Обменять ресурсы",
    "sell": "Продать ресурсы",
    "craft": "Скрафтить предмет",
    "dismantle": "Разобрать предмет",
    "dungeon (dung)": "Войти в данж текущей зоны",
    "enchant": "Зачаровать меч или броню (доступно со 2 зоны)",
    "-": "Команды для сохранения и выхода",
    "save": "Сохранить прогресс",
    "exit": "Выйти из игры"
}

while True:
    command = input("Введите команду: ").strip().lower()
    current_time = time.time()

    if command in ["help", "h"]:
        print("Список команд:")
        for cmd, desc in commands.items():
            print(f"{cmd}: {desc}")
        print()
    elif command == "shop":
        shop(player)
        print()
    elif command in ["profile", "p"]:
        player.show_profile()
        print()
    elif command in ["inventory", "i"]:
        player.show_inventory()
        print()
    elif command == "recipe":
        player.view_recipes()
        print()
    elif command.startswith("recipe craft"):
        item = command.split()[2]
        craft_recipe(player, item)
        print()
    elif command == "hunt":
        if current_time >= cooldowns["hunt"]:
            player.hunt()
            cooldowns["hunt"] = current_time + 30
        else:
            remaining = int(cooldowns["hunt"] - current_time)
            print(f"Команда 'hunt' будет доступна через {remaining} секунд.")
        print()
    elif command == "fish":
        if current_time >= cooldowns["fish"]:
            player.fish(command)
            cooldowns["fish"] = current_time + 90
        else:
            remaining = int(cooldowns["fish"] - current_time)
            print(f"Команда 'fish' будет доступна через {remaining} секунд.")
        print()
    elif command == "chop":
        if current_time >= cooldowns["chop"]:
            player.chop_tree(command)
            cooldowns["chop"] = current_time + 90
        else:
            remaining = int(cooldowns["chop"] - current_time)
            print(f"Команда 'chop' будет доступна через {remaining} секунд.")
        print()
    elif command == "collect":
        if current_time >= cooldowns["collect"]:
            player.collect(command)
            cooldowns["collect"] = current_time + 60
        else:
            remaining = int(cooldowns["collect"] - current_time)
            print(f"Команда 'collect' будет доступна через {remaining} секунд.")
        print()
    elif command == "mine":
        if current_time >= cooldowns["mine"]:
            player.mine()
            cooldowns["mine"] = current_time + 1200  # 20 минут
        else:
            remaining = int(cooldowns["mine"] - current_time)
            print(f"Команда 'mine' будет доступна через {remaining} секунд.")
        print()
    elif command == "daily":
        player.daily()
        print()
    elif command in ["cd", "cooldown"]:
        for action, cooldown in cooldowns.items():
            remaining = max(0, int(cooldown - current_time))
            if remaining == 0:
                print(f"Команда '{action}' готова.")
            else:
                print(f"Команда '{action}' будет доступна через {remaining} секунд.")
        print()
    elif command.startswith("trade"):
        parts = command.split()
        if len(parts) == 1:
            print("Обмен ресурсов:")
            print("1. 1 рыба на 2 древесины")
            print("2. 2 древесины на 1 рыбу")
            print("3. 6 древесины на 1 яблоко")
            print("4. 3 рыбы на 1 яблоко")
            print("5. 1 яблоко на 6 древесины")
            print("6. 1 яблоко на 3 рыбы")
        elif len(parts) == 2:
            player.trade(parts[1])
        elif len(parts) == 3:
            player.trade(parts[1], int(parts[2]))
        print()
    elif command.startswith("sell"):
        parts = command.split()
        if len(parts) == 1:
            print("Продажа ресурсов:")
            print("1. Продать рыбу (20 монет за штуку)")
            print("2. Продать золотую рыбу (200 монет за штуку)")
            print("3. Продать древесину (10 монет за штуку)")
            print("4. Продать эпическое дерево (150 монет за штуку)")
            print("5. Продать яблоки (50 монет за штуку)")
            print("6. Продать бананы (300 монет за штуку)")
        elif len(parts) == 3:
            player.sell(parts[1], int(parts[2]))
        print()
    elif command.startswith("craft"):
        parts = command.split()
        if len(parts) == 1:
            print("Крафт предметов:")
            print("1. Золотая рыба (15 рыбы)")
            print("2. Эпическое дерево (15 древесины)")
            print("3. Банан (6 яблок)")
        elif len(parts) == 3:
            item_map = {
                "1": "golden_fish",
                "2": "epic_wood",
                "3": "banana",
                "golden fish": "golden_fish",
                "epic log": "epic_wood",
                "banana": "banana"
            }
            item = item_map.get(parts[1], parts[1])
            if item in item_map.values():
                player.craft(item, int(parts[2]))
            else:
                print("Неверный предмет для крафта.")
        print()
    elif command.startswith("dismantle"):
        parts = command.split()
        if len(parts) == 1:
            print("Разборка предметов:")
            print("1. Золотая рыба (получите 11 рыбы)")
            print("2. Эпическое дерево (получите 11 древесины)")
            print("3. Банан (получите 4 яблока)")
        elif len(parts) == 3:
            item_map = {
                "1": "golden_fish",
                "2": "epic_wood",
                "3": "banana",
                "golden fish": "golden_fish",
                "epic log": "epic_wood",
                "banana": "banana"
            }
            item = item_map.get(parts[1], parts[1])
            if item in item_map.values():
                player.dismantle(item, int(parts[2]))
            else:
                print("Неверный предмет для разборки.")
        print()
    elif command in ["dungeon", "dung"]:
        current_time = time.time()
        if current_time < cooldowns["dungeon"]:
            remaining_hours = int((cooldowns["dungeon"] - current_time) / 3600)
            remaining_minutes = int(((cooldowns["dungeon"] - current_time) % 3600) / 60)
            print(f"Данж будет доступен через {remaining_hours} часов и {remaining_minutes} минут.")
            continue

        key_names = {1: "zone_1_key", 2: "zone_2_key", 3: "zone_3_key"}
        key_name = key_names.get(player.zone)

        if key_name is None or player.inventory.get(key_name, 0) < 1:
            print(f"У вас нет ключа для входа в данж зоны {player.zone}!")
            continue

        confirm = input(f"Вы уверены, что хотите войти в данж зоны {player.zone}? (y/n): ").lower()
        if confirm not in ['y', 'yes']:
            print("Вы решили не входить в данж.")
            continue

        player.dungeon()
        if player.hp > 0:  # Устанавливаем кулдаун только если игрок выжил
            cooldowns["dungeon"] = current_time + 86400  # 24 часа в секундах
        print()
    elif command == "save":
        save_progress(player)
        print()
    elif command == "exit":
        save_progress(player)
        print("Выход из игры. Прогресс сохранен.")
        break
    else:
        print("Неизвестная команда.")
        print()

if __name__ == "__main__":
    main()
