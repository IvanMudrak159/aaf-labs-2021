import Database
import CLI
import bst

def main():
    db = Database.Database()
    cli = CLI.CLI(db)
    cli.run()

def x():
    tree = bst.BST()
    tree.insert(1)
    tree.insert(5)
    tree.insert(3)

if __name__ == '__main__':
    x()
