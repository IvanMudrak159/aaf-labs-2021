import Database
import CLI


def main():
    db = Database.Database()
    cli = CLI.CLI(db)
    cli.run()


if __name__ == '__main__':
    main()
