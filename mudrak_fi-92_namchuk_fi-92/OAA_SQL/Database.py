import Table

class Database():
    def __init__(self):
        self.tables = []
        self.current_table = None

    def check_table_presence(self, table_name):
        for table in self.tables:
            if table_name == table.name:
                self.current_table = table
                return True
        return False

    def create(self, table_name, args):
        if self.check_table_presence(table_name):
            print("Table with such name already exist. Please try another name")
        else:
            table = Table.Table(table_name, args)
            self.tables.append(table)
            print('Table {0} has been created'.format(table_name))

    def insert(self, table_name, args):
        if self.check_table_presence(table_name):
            self.current_table.insert(args)
        else:
            print("Table with such name doesn't exist.")

    def select(self, table_name, columns, *args):
        if self.check_table_presence(table_name):
            self.current_table.select(columns, *args)
        else:
            print("Table with such name doesn't exist.")

    def delete(self, table_name):
        if self.check_table_presence(table_name):
            #TODO: delete table
            print('Table {0} has been deleted'.format(table_name))
        else:
            print("Table with such name doesn't exist.")