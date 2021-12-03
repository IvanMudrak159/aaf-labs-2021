import Database
import CLI

def main():
    db = Database.Database()
    cli = CLI.CLI(db)
    # db.create('map', ['id_person', 'name', 'position_ref'], [])
    # db.insert('map', ['1','Владимир','1'])
    # db.insert('map', ['2','Татьяна', '2'])
    # db.insert('map', ['3','Александр', '6'])
    # db.insert('map', ['4','Борис', '2'])
    # db.create('map2', ['id_pos', 'title'], [])
    # db.insert('map2', ['1', 'Дизайнер'])
    # db.insert('map2', ['2', 'Редактор'])
    # db.insert('map2', ['3', 'Программист'])
    # db.select('map', ['*'])
    # db.select('map2', ['*'])
    cli.run()

def x():
    x = [0,1]
    y = [1,2]
    print(x + y)

if __name__ == '__main__':
    main()
