import time
import random

class Character:
        skill_points = 2
        healing_flask = 1
        is_won = False

        def __init__(self, health, NormalAttack, ChargedAttack, ultimate, weapon):
            self.health = health
            self.NormalAttack = NormalAttack
            self.ChargedAttack = ChargedAttack
            self.ultimate = ultimate
            self.weapon = weapon
            self.charged = 0
            self.max_health = health

        def player_attributes(self):
            print(f"Hp: {self.health}, Normal attack Dmg: {self.NormalAttack}, Charged attack Dmg: {self.ChargedAttack}, ultimate: {self.ultimate}, weapon: {self.weapon}")

        def normal_attack(self, target):
            if Character.skill_points >= 1:
                Character.skill_points -= 1
                chance = random.randint(1, 5)
                if chance == 1 or chance == 5:
                    print("Critical Hit")
                    target.health -= self.NormalAttack * 2
                else:
                    target.health -= self.NormalAttack
                self.charged += 25
            else:
                print("Not enough skill points, skipping the round...")

        def charged_attack(self, target):
            if Character.skill_points >= 2:
                Character.skill_points -= 2
                chance = random.randint(1, 5)
                if chance == 1 or chance == 5:
                    print("Critical Hit")
                    target.health -= self.ChargedAttack * 2
                else:
                    target.health -= self.ChargedAttack
                self.charged += 30
            else:
                print("Not enough skill points, Using normal attack instead...")
                self.normal_attack(target)
                Character.skill_points -= 1

        def heal(self):
            if Character.healing_flask == 1:
                print("Healing...")
                time.sleep(1)
                self.health += 30
                Character.healing_flask = 0
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
                self.normal_attack(target)
                Character.skill_points -= 1

        def display_health(self, target):
            if self.health < 0:
                self.health = 0
                print("You Lost")
            if target.health < 0:
                target.health = 0
                print("You Won")
                Character.is_won = True
            if  self.health > 0 and target.health > 0:
                print(f"Your current health: {self.health}")
                print(f"boss current health: {target.health}")
                print(f"current skill points: {Character.skill_points}")

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
        print(f"1. Normal Attack ({player.NormalAttack} dps)")
        print(f"2. Charged Attack ({player.ChargedAttack} dps)")
        print("3. Heal (20 hp)")
        print(f"4. Ultimate ({player.charged}%), ({player.ultimate} dps)")

        while True:
            user_input = input("Choose an action: ").strip()
            if user_input in ['1', '2', '3', '4']:
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
    swordman = Character(100, 18, 24,35, "Sword")
    archer = Character(90, 16, 23, 32, "Bow")
    vagabond = Character(110, 20, 25, 33, "Great Sword")
    samurai = Character(95, 20, 24, 35, "Katana")
    wizard = Character(80, 17, 22, 40, "Magic")

    boss = Enemy("Zioles",125, 22, 30, "spear", 26)


    print("-------------")
    print(f"1.Sword Man:", end=" ")
    swordman.player_attributes()
    print(f"2.Archer:", end=" ")
    archer.player_attributes()
    print(f"3.Vagabond:", end=" ")
    vagabond.player_attributes()
    print(f"4.Samurai:", end=" ")
    samurai.player_attributes()
    print(f"5.Wizard:", end=" ")
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
                player.normal_attack(boss)
            case 2:
                player.charged_attack(boss)
            case 3:
                player.heal()
            case 4:
                player.activate_ultimate(boss)

        print()
        player.display_health(boss)
        Character.skill_points += 1

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

    if Character.is_won:
        player.health = player.max_health
        print()
        print(f"Congrats For Beating {boss.name}")
        print(f"You can choose between: ")
        print(f"1. {boss.name}'s {boss.weapon}")
        print(f"2. 3 Experience points")
        upgrade = int(input("Enter your choice: "))
        print()

        match upgrade:
            case 1:
                print(f"Your new weapon is: {boss.weapon}")
                player.weapon = boss.weapon
                print(f"Increased Dmg by 7+")
                player.NormalAttack += 7
                player.ChargedAttack += 7
                player.ultimate += 7
            case 2:
                print("You Gained 3 Experience points ")
                exp = 3
                print("You are able to Increase your stats: ")
                while exp > 0:
                    print("1.Dmg")
                    print("2.Hp")
                    print("3.accuracy")
                    print("4.dexterity")
                    print("5.save my Exp")
                    print()
                    upgrade = int(input("What stat you wanna upgrade: "))

                    match upgrade:
                        case 1:
                            player.NormalAttack += 5
                            player.ChargedAttack += 5
                            player.ultimate += 5
                            exp -= 1
                        case 2:
                            player.health += 4
                            exp -= 1
                        case 3:
                            if player == archer or player == wizard:
                                player.NormalAttack += 6
                                player.ChargedAttack += 6
                            else:
                                player.NormalAttack += 1
                                player.ChargedAttack += 1
                            exp -= 1
                        case 4:
                            if player == swordman or player == vagabond or player == samurai:
                                player.NormalAttack += 4
                                player.ChargedAttack += 4
                            else:
                                player.NormalAttack += 1
                                player.ChargedAttack += 1
                            exp -= 1
                        case 5:
                            print(f"Saving experience, current exp points: {exp}")
                            break
                print("Your new attributes is :")
                player.player_attributes()

if __name__ == '__main__':
    main()
