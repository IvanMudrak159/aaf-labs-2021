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

    def select(self, columns, left_token = None, operator = None, right_token = None):
        if columns == ['*']:
            columns = self.columns
        select_condition = self.empty()
        if left_token and operator and right_token:
            select_condition = self.condition(left_token, right_token, operator)
            for token in [left_token, right_token]:
                if token.type == "Column":
                    if not self.check_columns_presence(token.value):
                        return
        if self.check_columns_presence(columns):
            indexes = []
            for col in columns:
                indexes.append(self.get_column_index(col))
            table = PrettyTable(columns)
            #TODO: rename empty func
            for i in range(len(self.values[0]) - 1):
                if select_condition(i + 1):
                    value = []
                    for index in indexes:
                        value.append(self.values[index][i+1])
                    table.add_row(value)
            print(table)

    def delete(self, left_token = None, operator = None, right_token = None):
        delete_condition = self.condition(left_token, right_token, operator)
        indexes = []
        for i in range(len(self.values[0]) - 1):
            if delete_condition(i + 1):
                indexes.append(i + 1)
        line_index = len(indexes) - 1
        deleted_rows = len(indexes)
        while line_index >= 0:
            for column_index in range(len(self.values)):
                self.values[column_index].pop(indexes[line_index])
            line_index -= 1
        if deleted_rows == 1:
            print("{0} row has been deleted".format(deleted_rows))
        else:
            print("{0} rows have been deleted".format(deleted_rows))

    def empty(self):
        return lambda i: True

    def condition(self, left_token, right_token, operator):
        if left_token.type == "Value":
            if right_token.type == "Value":
                return lambda i: ops[operator](left_token.value, right_token.value)
            else:
                index = self.get_column_index(right_token.value)
                return lambda i: ops[operator](left_token.value, self.values[index][i])
        else:
            if right_token.type == "Value":
                index = self.get_column_index(left_token.value)
                return lambda i: ops[operator](self.values[index][i], right_token.value)
            else:
                l_index = self.get_column_index(left_token.value)
                r_index = self.get_column_index(right_token.value)
                return lambda i: ops[operator](self.values[l_index][i], self.values[r_index][i])

    def get_column_index(self, column):
        return self.columns.index(column)

    def check_columns_presence(self, columns):
        for el in columns:
            if el not in self.columns:
                print('Column name does not match table definition.')
                return False
        return True
