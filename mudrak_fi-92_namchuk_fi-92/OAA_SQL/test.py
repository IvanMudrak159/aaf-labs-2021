import Database
import CLI
import Index

def main():
    db = Database.Database()
    cli = CLI.CLI(db)
    cli.run()
def y(operator):
    if operator == "*":
        print(operator)
        return lambda a,b: a*b
    elif operator == "/":
        print(operator)
        return lambda a,b: a/b
def x():
    x = [[1,2,3],[4,5,6]]
    for i in range(len(x)):
        for y in range(len(x[i])):
            print(x[i][y])


if __name__ == '__main__':
    main()
