#!/usr/bin/env python3
# lib/debug.py

from models.__init__ import CONN, CURSOR
from models.Fight import Fight
from models.Fighter import Fighter
from models.Weight_class import Weight_class
from helpers import *
import ipdb

Weight_class.drop_table()
Fighter.drop_table()
Fight.drop_table()
Weight_class.create_table()
Fighter.create_table()
Fight.create_table()

Weight_class.create(125, "flyweight")
Weight_class.create(135, "bantamweight")
Weight_class.create(145, "featherweight")

Fighter.create("Mighty Mouse", 35, 1, 20, 5)
Fighter.create("Assassin Baby", 32, 1, 15, 3)
Fighter.create("Max Holloway", 32, 3, 30, 0)
Fighter.create("Jose Aldo", 40, 3, 35, 7)

Fight.create("02/28/2024", 1, 2, 1)
Fight.create("09/09/2027", 3, 4, 3)

max = Fighter.find_by_name('Max Holloway')
fight = Fight.create('01/01/2924', 1, 2, 2)
ipdb.set_trace()


