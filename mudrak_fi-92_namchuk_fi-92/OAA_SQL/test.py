import Database
import CLI
import Index

def main():
    db = Database.Database()
    cli = CLI.CLI(db)
    cli.run()
    db.create('map', ['x','y'], [0])

def y():
    db = Database.Database()
    cli = CLI.CLI(db)
    # db.create('map', ['x', 'y'], [0,1])
    # db.insert('map', ['1', '2'])
    # db.insert('map', ['3', '14'])
    # db.insert('map', ['5', '6'])
    # db.select('map', ['x','y'])
    cli.run()

def x():
    x = [0,1]
    for i in x:
        print(i)

if __name__ == '__main__':
    y()
