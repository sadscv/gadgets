#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17-3-30 上午8:19
# @Author  : sadscv
# @File    : Factory.py

#Burger class
class Burger():
    name=""
    price = 0.0
    def getPrice(self):
        return self.price
    def setPrice(self, price):
        self.price = price
    def getName(self):
        return self.name

class cheeseBurger(Burger):
    def __init__(self):
        self.name = "chess burger"
        self.price  = 10.0

class spicyChickenBurger(Burger):
    def __init__(self):
        self.name = "spicy chicken burger"
        self.price = 15.0

#Snack class
class Snack():
    name = ""
    price = 0.0
    type = "SNACK"
    def getPrice(self):
        return self.price
    def setPrice(self, price):
        self.price = price
    def getName(self):
        return self.name


class chips(Snack):
    def __init__(self):
        self.name = "chips"
        self.price = 6.0


class chickenWings(Snack):
    def __init__(self):
        self.name = "chicken wings"
        self.price = 12.0

#Beverage class
class Beverage():
    name = ""
    price = 0.0
    type = "BEVERAGE"
    def getPrice(self):
        return self.price
    def setPrice(self, price):
        self.price = price
    def getName(self):
        return self.name


class coke(Beverage):
    def __init__(self):
        self.name = "coke"
        self.price = 4.0


class milk(Beverage):
    def __init__(self):
        self.name = "milk"
        self.price = 5.0


class foodFactory():
    type = ""
    def createFood(self, foodclass):
        print(self.type, "factory produce a instance.")
        foodIns = foodclass()
        return foodIns

class burgerFactory(foodFactory):
    def __init__(self):
        self.type = "BURGER"

class snackFactory(foodFactory):
    def __init__(self):
        self.type = "SNACK"

class beverageFactory(foodFactory):
    def __init__(self):
        self.type="BEVERAGE"



if  __name__=="__main__":
    burger_factory=burgerFactory()
    snack_factorry=snackFactory()
    beverage_factory=beverageFactory()
    cheese_burger=burger_factory.createFood(cheeseBurger)
    print (cheese_burger.getName(),cheese_burger.getPrice())
    chicken_wings=snack_factorry.createFood(chickenWings)
    print (chicken_wings.getName(),chicken_wings.getPrice())
    coke_drink=beverage_factory.createFood(coke)
    print (coke_drink.getName(),coke_drink.getPrice())
