import random
from src import Collections
import time



class Person:
    def __init__(self, name, profession, intelligence, money, car, property, mother,
                 father, siblings, happiness, location, age, currenteducation, education,
                 health, illness, cureAttemptByTurn, looks, actionLimit, currentActions, healthDecay,
                 intelligenceDecay, birthDefects, relationships, isHealthy, isHealthyTurns, eventCooldown,
                 strength, strengthDecay, happinessDecay, job, debug, timeAtJob, timeAtJobHolder):
        self.name = name
        self.profession = profession
        self.intelligence = intelligence
        self.money = money
        self.car = car
        self.property = property
        self.mother = mother
        self.father = father
        self.siblings = siblings
        self.happiness = happiness
        self.location = location
        self.age = age
        self.currenteducation = currenteducation
        self.education = education
        self.health = health
        self.illness = illness
        self.cureAttemptByTurn = cureAttemptByTurn
        self.looks = looks
        self.actionLimit = actionLimit
        self.currentActions = currentActions
        self.healthDecay = healthDecay
        self.intelligenceDecay = intelligenceDecay
        self.birthDefects = birthDefects
        self.relationships = relationships
        self.isHealthy = isHealthy
        self.isHealthyTurns = isHealthyTurns
        self.eventCooldown = eventCooldown
        self.strength = strength
        self.strengthDecay = strengthDecay
        self.happinessDecay = happinessDecay
        self.memorizeTurns = 0
        self.highSchoolIntelligenceDecay = 0
        self.job = job
        self.debug = debug
        self.timeAtJob = timeAtJob
        self.timeAtJobHolder = timeAtJobHolder


    def calculateHealth(self):
        if self.isHealthyTurns > 0:
            self.isHealthy = True
            self.isHealthyTurns = self.isHealthyTurns - 1
        else:
            self.isHealthy = False
        if self.illness == None:
            illnessChance = (100 - self.health) // 20 + 2
            if self.isHealthy == False:
                if random.randint(1, 100) <= illnessChance:
                    self.illness = Collections.getRandomIllness()
                    print("You have contracted " + self.illness.name)
                    self.health -= self.healthDecay
                if self.illness != None and self.age >= 65:
                    if random.randint(1,1000) == 1:
                        self.illness = Collections.alzheimers
                        print("You have contracted " + self.illness.name)
                        self.health = self.health - self.healthDecay
        else:
            self.health -= self.illness.healthDecay
            self.happiness -= self.illness.happinessDecay
            self.intelligence -= self.illness.intelligenceDecay
            if self.health <= 0:
                print("You have died")
                exit()
        
        self.healthDecay = self.memorizeTurns / 2
        
        ageHealthDecay = 0
        
        if self.age > 90:
          ageHealthDecay = 2
        elif self.age > 80:
          ageHealthDecay = 1
        elif self.age > 70:
          ageHealthDecay = 0.5
        
        self.health -= self.healthDecay + ageHealthDecay
        
        if self.health <= 0:
            print("You have died")
            exit()
        
        if self.age >= 12 and self.happiness <= 0:
            print("Your life is ruined by bad decisions, you feel everyone is out to get you, you can't get a break, but you'll make one. You kill yourself.")
            exit()

    def calculateIntelligence(self):
        if self.age < 16:
            self.intelligenceDecay = 0
        else:
            self.intelligenceDecay = 0.5
        self.intelligence -= self.intelligenceDecay + self.highSchoolIntelligenceDecay
        if self.intelligence < 0:
            self.intelligence = 0

    def calculateBirthDefects(self):
        if len(self.birthDefects) == 1:
            self.healthDecay -= self.birthDefects[0]
        elif len(self.birthDefects) == 2:
            self.healthDecay -= (self.birthDefects[0] + self.birthDefects[1])

    def calculateRelationshipValues(self):
        for i in self.relationships:
            i.calculateRelationship()



    def checkAge(self):
        self.actionLimit = 5
        if self.age >= 5:
            self.currenteducation = "Elementary School"
            self.actionLimit = 5
        if self.age >= 11:
            self.currenteducation = "Middle School"
            self.actionLimit = 6
        if self.age >= 14:
            self.currenteducation = "High School"
            self.actionLimit = 7
        if self.age >= 18:
            self.currenteducation = "Not Enrolled"
            self.actionLimit = 8
        if self.age >= 22 and self.education == "Bachelors":
            print("You just finished undergrad school, you can go to grad school.")

    def visitDoctorIllness(self):
        if self.cureAttemptByTurn > 0:
            self.cureAttemptByTurn = self.cureAttemptByTurn - 1
            print("you only have " + str(self.cureAttemptByTurn) + " attempts left, now!")
            if self.age < 18:
                if self.relationships[0].status == "Low Income":
                    chance = 30
                elif self.relationships[0].status == "Mid Income":
                    chance = 50
                else:
                    chance = 80
                if randint(1, 100) <= chance:
                    print("Your parents decide to take you to treatment for " + self.illness.name)
                    print("It costed them $" + str(self.illness.cureCost))
                    curechance = random.randint(1, 100)
                    if curechance < self.illness.cureChance:
                        print("You have cured " + self.illness.name)
                        self.illness = None
                    else:
                        print(
                            "The doctors provided the best treatment possible, but they were unable to come to a cure.")
                        # Add doctor variation of skill and cost
                        # add the amount of treatments needs to cure a specific disease/illness
                else:
                    print(f"Your parents could not afford to take you to the doctor. {self.relationships[0].status}! They are devastated.")
            else:
                print("It will cost " + str(self.illness.cureCost) + " to cure " + self.illness.name)
                print("Would you like to attempt to cure? y/n")
                pinput = input()
                if pinput == "y":
                    if self.money >= self.illness.cureCost:
                        curechance = random.randint(1, 100)
                        if curechance < self.illness.cureChance:
                            self.health += 3 * self.illness.healthDecay
                            self.happiness += 3 * self.illness.happinessDecay
                            self.intelligence += 3 * self.illness.intelligenceDecay
                            
                            self.happiness = min(self.happiness, 100)
                            self.health = min(self.health, 100)
                            self.intelligence = min(self.intelligence, 100)
                            
                            print("You have cured " + self.illness.name)
                            
                            self.illness = None
                        else:
                            print("You recieved treatment but you continue to suffer from " + self.illness.name)
                            
                    else:
                        print("You do not have the money to go through treatment")
                        # add potential financing
        else:
            print("You don't have any more cure attempts this turn! Hope ya don't die!")
        time.sleep(1)

    def useAction(self):
        self.currentActions -= 1
        print("You used an action")
        print("you have " + str(self.currentActions) + " actions left out of " + str(self.actionLimit))

    def calculateStatDependencies(self):
        # no idea where to start here

        # Ensuring that decay doesn't enter negative nunbers
        if self.happinessDecay < 0:
            self.happinessDecay = 0
        if self.strengthDecay < 0:
            self.strengthDecay = 0
        if self.healthDecay < 0:
            self.healthDecay = 0
        if self.intelligenceDecay < 0:
            self.intelligenceDecay = 0

        relationshipHappinessDelta = 0
        avg = (self.relationships[0].relationshipvalue + self.relationships[1].relationshipvalue) / 2
        relationshipHappinessDelta = round(((avg - 50) / 50) * 2) / 2
        
        propertyHappinessDelta = self.property.happinessDelta
        
        self.happiness += relationshipHappinessDelta + propertyHappinessDelta
