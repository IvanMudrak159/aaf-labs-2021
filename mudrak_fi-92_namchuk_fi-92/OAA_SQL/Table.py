from prettytable import PrettyTable
import operator

ops = {
    '=': operator.eq,
    '!=': operator.ne,
    '<': operator.lt,
    '<=': operator.le,
    '>': operator.gt,
    '>=': operator.ge
}


class Table(object):
    def __init__(self, table_name, columns):
        self.name = table_name
        self.values = columns
        cols = []
        for el in columns:
            cols.append(el[0])
        self.columns = cols

    def insert(self, args):
        if len(args) == len(self.columns):
            for (column, arg) in zip(self.values, args):
                column.append(arg)
            print("1 row has been inserted into {0}.".format(self.name))
        else:
            print("Inconsistent number of values added to the table.")

    def select(self, columns, *args):
        if columns == ['*']:
            columns = self.columns
        selected_column = None
        operator = None
        const = None
        has_conditions = False
        if len(args) != 0:
            has_conditions = True
            if not self.check_columns_presence(args[0]):
                print('Column name does not match table definition.')
                return
            selected_column = self.get_column_index(args[0])[0]
            operator = args[1]
            const = args[2]
        if self.check_columns_presence(columns):
            indexes = self.get_column_index(columns)
            table = PrettyTable(columns)
            for i in range(len(self.values[0]) - 1):
                if not has_conditions or ops[operator](self.values[selected_column][i+1], const):
                    value = []
                    for index in indexes:
                        value.append(self.values[index][i+1])
                    table.add_row(value)
            print(table)
        else:
            print('Column name does not match table definition.')

    def get_column_index(self, columns):
        indexes = []
        for column in columns:
            indexes.append(self.columns.index(column))
        return indexes

    def check_columns_presence(self, columns):
        for el in columns:
            if el not in self.columns:
                return False
        return True
