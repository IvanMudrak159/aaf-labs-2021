import Table


class Database:
    def __init__(self):
        self.tables = []
        self.current_table = None

    def check_table_presence(self, table_name):
        for table in self.tables:
            if table_name == table.name:
                self.current_table = table
                return table
        return None

    def create(self, table_name, columns, columns_id):
        if self.check_table_presence(table_name):
            print("Table with such name already exist. Please try another name")
        else:
            table = Table.Table(table_name, columns, columns_id)
            self.tables.append(table)
            print('Table {0} has been created'.format(table_name))

    def insert(self, table_name, args):
        if self.check_table_presence(table_name):
            if self.current_table.insert(args):
                print("1 row has been inserted into {0}.".format(table_name))
        else:
            print("Table with such name doesn't exist.")

    def select(self, table_name, columns, second_table_name = None, left_column = None, right_column = None, left_token = None, operator = None, right_token = None):
        if self.check_table_presence(table_name):
            first_table = self.current_table
            if second_table_name is None:
                first_table.select(columns, second_table_name, left_column, right_column, left_token, operator, right_token)
            elif self.check_table_presence(second_table_name):
                second_table = self.current_table
                first_table.select(columns, second_table, left_column, right_column, left_token, operator, right_token)
            else:
                print("2.Table with such name doesn't exist.")
        else:
            print("1.Table with such name doesn't exist.")

    def delete(self, table_name, *args):
        if self.check_table_presence(table_name):
            self.current_table.delete(*args)
        else:
            print("Table with such name doesn't exist.")
