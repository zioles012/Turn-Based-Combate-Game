import time
import random

class Character:
    def __init__(self, health, damage, ultimate, weapon):
        self.health = health
        self.damage = damage
        self.ultimate = ultimate
        self.weapon = weapon
        self.healing_flask = 1
        self.charged = 0

    def player_attributes(self):
        print(f"Hp:{self.health}, Dmg:{self.damage}, ultimate:{self.ultimate}, weapon:{self.weapon}")

    def attack(self, target):
        chance = random.randint(1, 5)
        if chance == 1 or chance == 5:
            print("Critical Hit")
            target.health -= self.damage * 2
        else:
            target.health -= self.damage
        self.charged += 25

    def heal(self):
        if self.healing_flask == 1:
            print("Healing...")
            time.sleep(1)
            self.health += 30
            self.healing_flask = 0
        else:
            print("No healing flask has been found")

    def activate_ultimate(self, target):
        if self.charged >= 100:
            print("ACTIVATING ULTIMATE...")
            time.sleep(2)
            target.health -= self.ultimate
            self.charged = 0
            print(f"You dealt {self.ultimate} dmg")
        else:
            print("Ultimate is not ready, attacking the boss instead..")
            self.attack(target)

    def display_health(self, target):
        if self.health < 0:
            self.health = 0
            print("You Lost")
        if target.health < 0:
            target.health = 0
            print("You won")
        if  self.health > 0 and target.health > 0:
            print(f"Your current health: {self.health}")
            print(f"boss current health: {target.health}")

class Enemy:
    def __init__(self, name , health, damage, ultimate, weapon, special):
        self.name = name
        self.health = health
        self.damage = damage
        self.ultimate = ultimate
        self.weapon = weapon
        self.special = special
        self.charged = 0
        self.special_available = True
        self.max_health = health

    def enemy_attributes(self):
        print(f"The boss to fight is: {self.name} Hp: {self.health}")

    def attack(self, target):
        target.health -= self.damage
        self.charged += 24

    def special_ability(self, target):
        target.health -= self.special
        self.health += 10
        self.charged += 25

    def ultimate_ability(self, target):
        print("ACTIVATING BOSS ULTIMATE...")
        time.sleep(2)
        target.health -= self.ultimate
        print(f"the boss dealt {self.ultimate} dmg")
        self.charged -= 100

def player_turn(player):
    print()
    print("It's your turn: ")
    time.sleep(1)
    print(f"1.Attack ({player.damage} dps)")
    print("2.Heal (20 hp)")
    print(f"3.Ultimate ({player.charged}%)")

    while True:
        user_input = input("Choose an action: ").strip()
        if user_input in ['1', '2', '3']:
            return int(user_input)
        else:
            print("Invalid input, choose 1, 2, or 3.")

def boss_turn(boss, player):
    if boss.health < 0.3 * boss.max_health and boss.special_available:
        Action = "special"
        boss.special_available = False

    elif player.health <= boss.ultimate and boss.charged >= 100:
        Action = "ultimate"

    else:
        Action = random.choice(["attack", "attack", "attack", "special"])
    return Action

def main():
    swordman = Character(100, 20, 35, "Sword")
    archer = Character(90, 18, 30, "Bow")
    vagabond = Character(110, 25, 32, "Great Sword")
    samurai = Character(95, 22, 33, "Katana")
    wizard = Character(80, 15, 40, "Magic")

    boss = Enemy("Zioles",125, 22, 30, "spear", 26)

    print("-------------")
    print(f"1.sword man", end=" ")
    swordman.player_attributes()
    print(f"2.archer", end=" ")
    archer.player_attributes()
    print(f"3.vagabond", end=" ")
    vagabond.player_attributes()
    print(f"4.samurai", end=" ")
    samurai.player_attributes()
    print(f"5.wizard", end=" ")
    wizard.player_attributes()
    print("-------------")
    player = int(input("Enter a character: "))

    match player:
        case 1:
            player = swordman
            print("You chose to be a 'Sword Man'.")
        case 2:
            player = archer
            print("You chose to be an 'Archer'.")
        case 3:
            player = vagabond
            print("You chose to be a 'Vagabond'.")
        case 4:
            player = samurai
            print("You chose to be a 'Samurai'.")
        case 5:
            player = wizard
            print("You chose to be a 'Wizard'.")
    print()
    boss.enemy_attributes()

    while player.health > 0 and boss.health > 0:
        choice = player_turn(player)
        match choice:
            case 1:
                player.attack(boss)
            case 2:
                player.heal()
            case 3:
                player.activate_ultimate(boss)

        print()
        player.display_health(boss)
        if player.health <= 0 or boss.health <= 0:
            break

        print()
        print("It's the boss turn: ")
        time.sleep(2)

        action = boss_turn(boss, player)
        match action:
            case "attack":
                print(f"{boss.name} chose to attack")
                time.sleep(1)
                boss.attack(player)

            case "special":
                print(f"{boss.name} is performing his special ability 'spear throw'")
                time.sleep(1)
                boss.special_ability(player)

            case "ultimate":
                print(f"{boss.name} is charging up his ultimate against you")
                boss.ultimate_ability(player)

        print()
        player.display_health(boss)
        if player.health <= 0 or boss.health <= 0:
            break

if __name__ == '__main__':
    main()