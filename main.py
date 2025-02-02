from aotree import Tree


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

    tree.add_or_connection("A", "B")
    tree.add_and_connection("A", "C", "D")
    tree.add_or_connection("B", "E", "F")
    tree.add_or_connection("C", "G")
    tree.add_and_connection("C", "H", "I")
    tree.add_or_connection("D", "J")

    tree.update_cost("A")
    tree.show_shortest_path("A")


if __name__ == "__main__":
    main()
