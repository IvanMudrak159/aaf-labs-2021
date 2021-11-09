import Table

class Database():
    def __init__(self):
        self.tables = []

    def create(self, table_name, args):
        print('Table {0} has been created'.format(table_name))
        table = Table.Table(table_name, args)
        self.tables.append(table)

    def insert(self, table_name, table_values):
        print('Values have been added to {0}'.format(table_name))

    def delete(self, table_name):
        print('Table {0} has been deleted'.format(table_name))