#!/usr/bin/env python3

from models.__init__ import CONN, CURSOR
from models.Weight_class import Weight_class
from models.Fighter import Fighter
from models.Fight import Fight


def main():
    Weight_class.drop_table()
    Fighter.drop_table()
    Fight.drop_table()
    Weight_class.create_table()
    Fighter.create_table()
    Fight.create_table()

    Weight_class.create(125, "Flyweight")
    Weight_class.create(135, "Bantamweight")
    Weight_class.create(145, "Featherweight")

    Fighter.create("Mighty Mouse", 35, 1, 20, 5)
    Fighter.create("Assassin Baby", 32, 1, 15, 3)
    Fighter.create("Aljamain Sterling", 29, 2, 20, 5)
    Fighter.create("Henry Cejudo", 31, 2, 16, 3)
    Fighter.create("Max Holloway", 32, 3, 30, 0)
    Fighter.create("Jose Aldo", 40, 3, 35, 7)

    Fight.create("02/28/2024", 1, 2, 1)
    Fight.create("09/09/2022", 3, 4, 3)
    Fight.create("09/09/2022", 1, 2, 2)
    Fight.create("04/27/2007", 3, 4, 3)


if __name__ == "__main__":
    main()