from models.__init__ import CONN, CURSOR
from models.Weight_class import Weight_class


def main():
    Weight_class.drop_table()
    Weight_class.create_table()

    Weight_class.create(125, "flyweight")
    Weight_class.create(135, "bantamweight")
    Weight_class.create(145, "featherweight")

if __name__ == "__main__":
    main()