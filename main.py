from aograph import Tree


def main():
    nodes = {
        "A": -1.0,
        "B": 5.0,
        "C": 2.0,
        "D": 4.0,
        "E": 7.0,
        "F": 9.0,
        "G": 3.0,
        "H": 0.0,
        "I": 0.0,
        "J": 0.0,
    }
    tree = Tree(nodes)

    tree.print()


if __name__ == "__main__":
    main()
