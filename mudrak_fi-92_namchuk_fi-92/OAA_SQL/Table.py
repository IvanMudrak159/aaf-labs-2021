from prettytable import PrettyTable
import operator
import Index

ops = {
    '=': operator.eq,
    '!=': operator.ne,
    '<': operator.lt,
    '<=': operator.le,
    '>': operator.gt,
    '>=': operator.ge
}

class Table(object):
    def __init__(self, table_name, columns, columns_id):
        self.name = table_name

        self.id = 0
        self.values = {}

        self.columns = columns

        self.indexes = []
        for id in columns_id:
            self.indexes.append(Index.Index(id))

    def insert(self, values):
        if len(values) == len(self.columns):
            self.values[self.id] = values
            self.id += 1

            for index in self.indexes:
                index.insert(values[index.id], self.id - 1)
            print("1 row has been inserted into {0}.".format(self.name))
        else:
            print("Inconsistent number of values added to the table.")

    def select(self, columns, left_token = None, operator = None, right_token = None):
        if columns == ['*']:
            columns = self.columns
        if left_token and operator and right_token:
            select_condition = self.condition(left_token, right_token, operator)
            result = self.define(left_token, right_token)
            if result == 0:
                return
            elif result == 1:
                #l and r = value
                self.print_table(columns, select_condition, self.values.keys())
            elif result == 2:
                #l = value, r = column
                index = self.get_index(right_token)
                if index:
                    row_indexes = index.get_lines(self.invert_operator(operator), left_token.value)
                    self.print_table(columns, self.true(), row_indexes)
                else:
                    self.print_table(columns, select_condition, self.values.keys())
            elif result == 3:
                #l = column, r = value
                index = self.get_index(left_token)
                if index:
                    row_indexes = index.get_lines(operator, right_token.value)
                    self.print_table(columns, self.true(), row_indexes)
                else:
                    self.print_table(columns, select_condition, self.values.keys())
            else:
                # l = column, r = column
                self.print_table(columns, select_condition, self.values.keys())
        else:
            self.print_table(columns, self.true(), self.values.keys())

    def get_index(self, token):
        for index in self.indexes:
            if self.columns[index.id] == token.value:
                return index
        return None

    def invert_operator(self, operator):
        if operator == '>':
            return '<'
        elif operator == '<':
            return '>'
        elif operator == '<=':
            return '>='
        elif operator == '>=':
            return '<='
        else:
            return operator

    def print_table(self, columns, select_condition, row_indexes):
        if self.check_columns_presence(columns):
            indexes = []
            for col in columns:
                indexes.append(self.get_column_index(col))
            table = PrettyTable(columns)
            for i in row_indexes:
                if select_condition(i):
                    value = []
                    for index in indexes:
                        value.append(self.values[i][index])
                    table.add_row(value)
            print(table)

    def delete(self, left_token = None, operator = None, right_token = None):
        delete_condition = self.condition(left_token, right_token, operator)
        deleted_rows = 0
        result = self.define(left_token, right_token)

        lines = []
        if result == 0:
            print('Error')
            return
        elif result == 1:
            # l and r = value
            if delete_condition(0):
                delete_condition = self.true()
            else:
                delete_condition = self.false()
            lines = list(self.values)
        elif result == 2:
            # l = value, r = column
            index = self.get_index(right_token)
            if index:
                lines = index.get_lines(self.invert_operator(operator), left_token.value)
        elif result == 3:
            # l = column, r = value
            index = self.get_index(left_token)
            if index:
                lines = index.get_lines(operator, right_token.value)
        else:
            # l = column, r = column
            lines = list(self.values)

        for i in list(self.values):
            if delete_condition(i):
                deleted_rows += 1
                del self.values[i]
        if deleted_rows == 1:
            print("{0} row has been deleted".format(deleted_rows))
        else:
            print("{0} rows have been deleted".format(deleted_rows))

    def define(self,left_token, right_token):
        for token in [left_token, right_token]:
            if token.type == "Column":
                if not self.check_columns_presence(token.value):
                    return 0
        if left_token.type == "Value":
            if right_token.type == "Value":
                return 1
            else:
                return 2
        else:
            if right_token.type == "Value":
                return 3
            else:
                return 4

    def true(self):
        return lambda i: True

    def false(self):
        return lambda i: False
    def condition(self, left_token, right_token, operator):
        if left_token.type == "Value":
            if right_token.type == "Value":
                return lambda i: ops[operator](left_token.value, right_token.value)
            else:
                index = self.get_column_index(right_token.value)
                return lambda i: ops[operator](left_token.value, self.values[i][index])
        else:
            if right_token.type == "Value":
                index = self.get_column_index(left_token.value)
                return lambda i: ops[operator](self.values[i][index], right_token.value)
            else:
                l_index = self.get_column_index(left_token.value)
                r_index = self.get_column_index(right_token.value)
                return lambda i: ops[operator](self.values[i][l_index], self.values[i][r_index])

    def get_column_index(self, column):
        return self.columns.index(column)

    def check_columns_presence(self, columns):
        for el in columns:
            if el not in self.columns:
                print('Column name does not match table definition.')
                return False
        return True