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
            return True
        else:
            print("Inconsistent number of values added to the table.")

    def select(self, columns, second_table = None, left_column = None, right_column = None, left_token = None, operator = None, right_token = None):
        if second_table:
            first_table_columns = []
            second_table_columns = []
            if columns == ['*']:
                first_table_columns = self.columns
                second_table_columns = second_table.columns
            else:
                for column in columns:
                    if self.check_columns_presence([column]):
                        first_table_columns.append(column)
                    elif second_table.check_columns_presence([column]):
                        second_table_columns.append(column)
                    else:
                        print('Column name does not match any table definition.')
                        return
            first_table_columns_id = []
            second_table_columns_id = []
            for id in first_table_columns:
                first_table_columns_id.append(self.get_column_index(id))
            for id in second_table_columns:
                second_table_columns_id.append(second_table.get_column_index(id))

            if left_column and right_column:
                if not self.check_columns_presence([left_column.value]) or not second_table.check_columns_presence([right_column.value]):
                    print('Invalid syntax in ON check.')
                    return
                left_column_id = self.get_column_index(left_column.value)
                right_column_id = second_table.get_column_index(right_column.value)
                new_table = Table('temp', first_table_columns + second_table_columns, [])

                join_index = None
                table_with_index = self
                table_without_index = second_table
                second_table_column_id = table_without_index.get_column_index(right_column.value)
                for index in self.indexes:
                    if index.id == left_column_id:
                        join_index = index
                        break
                if join_index is None:
                    for index in second_table.indexes:
                        if index.id == right_column_id:
                            join_index = index
                            table_with_index = second_table
                            table_without_index = self
                            second_table_column_id = table_without_index.get_column_index(left_column.value)
                            break
                if join_index is None:
                    return self.join_without_index(first_table_columns_id, left_column, left_token, new_table, operator,
                                                   right_column, right_token, second_table, second_table_columns_id)
                else:
                    return self.join_with_index(first_table_columns_id, join_index, left_token, new_table, operator,
                                                right_token, second_table_column_id, second_table_columns_id,
                                                table_with_index, table_without_index)


            else:
                new_table = Table('temp', first_table_columns + second_table_columns, [])
                for i in self.values.keys():
                    value = []
                    for id in first_table_columns_id:
                        value.append(self.values[i][id])
                    for j in second_table.values.keys():
                        temp_value = value[:]
                        for id in second_table_columns_id:
                            temp_value.append(second_table.values[j][id])
                        new_table.insert(temp_value)
                return new_table.select(['*'], left_token= left_token, operator= operator, right_token= right_token)

        if columns == ['*']:
            columns = self.columns

        if left_token and operator and right_token:
            select_condition = self.condition(left_token, right_token, operator)
            result = self.define(left_token, right_token)
            if result == 0:
                print('Error')
                return
            elif result == 1:
                #l and r = value
                self.print_table(columns, select_condition, self.values.keys())
            elif result == 2:
                #l = value, r = column
                index = self.get_index(right_token)
                if index and operator != '!=':
                    row_indexes = index.get_lines(self.invert_operator(operator), left_token.value)
                    self.print_table(columns, self.true(), row_indexes)
                else:
                    self.print_table(columns, select_condition, self.values.keys())
            elif result == 3:
                #l = column, r = value
                index = self.get_index(left_token)
                if index and operator != '!=':
                    row_indexes = index.get_lines(operator, right_token.value)
                    self.print_table(columns, self.true(), row_indexes)
                else:
                    self.print_table(columns, select_condition, self.values.keys())
            else:
                # l = column, r = column
                self.print_table(columns, select_condition, self.values.keys())
        else:
            self.print_table(columns, self.true(), self.values.keys())

    def join_with_index(self, first_table_columns_id, join_index, left_token, new_table, operator, right_token,
                        second_table_column_id, second_table_columns_id, table_with_index, table_without_index):
        for i in table_without_index.values.keys():
            lines = join_index.values.get(table_without_index.values[i][second_table_column_id])
            if lines is not None:
                for row_id in lines:
                    value = []
                    if table_with_index == self:
                        for first_table_id in first_table_columns_id:
                            value.append(table_with_index.values[row_id][first_table_id])
                        for second_table_id in second_table_columns_id:
                            value.append(table_without_index.values[i][second_table_id])
                    else:
                        for second_table_id in second_table_columns_id:
                            value.append(table_with_index.values[row_id][second_table_id])
                        for first_table_id in first_table_columns_id:
                            value.append(table_without_index.values[i][first_table_id])
                    new_table.insert(value)
        return new_table.select(['*'], left_token=left_token, operator=operator, right_token=right_token)

    def join_without_index(self, first_table_columns_id, left_column, left_token, new_table, operator, right_column, right_token,
                           second_table, second_table_columns_id):
        join_index = dict()
        smaller_table = second_table
        bigger_table = self
        key_column = second_table.get_column_index(right_column.value)
        value_column = self.get_column_index(left_column.value)
        if len(self.values) < len(second_table.values):
            smaller_table = self
            bigger_table = second_table
            key_column = smaller_table.get_column_index(left_column.value)
            value_column = bigger_table.get_column_index(right_column.value)

        for i in smaller_table.values.keys():
            key = smaller_table.values[i][key_column]
            if join_index.get(key) is None:
                join_index[key] = [i]
            else:
                join_index[key] += [i]

        row_count = 0

        for key in bigger_table.values.keys():
            value = []
            join_value = bigger_table.values[key][value_column]
            if join_index.get(join_value) is not None:
                if smaller_table == self:
                    for row_id in join_index[join_value]:
                        for id in first_table_columns_id:
                            value.append(self.values[row_id][id])
                        for id in second_table_columns_id:
                            value.append(second_table.values[key][id])
                        new_table.insert(value)
                        value = []
                else:
                    for row_id in join_index[join_value]:
                        for id in second_table_columns_id:
                            value.append(second_table.values[row_id][id])
                        for id in first_table_columns_id:
                            value.append(self.values[key][id])
                        new_table.insert(value)
                        value = []

        return new_table.select(['*'], left_token=left_token, operator=operator, right_token=right_token)

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
        else:
            print('Column name does not match table definition.')

    def delete(self, left_token = None, operator = None, right_token = None):
        delete_condition = self.true()
        deleted_rows = 0
        lines = list(self.values)
        if left_token and operator and right_token:
            delete_condition = self.condition(left_token, right_token, operator)
            result = self.define(left_token, right_token)

            if result == 0:
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
        for i in lines:
            if delete_condition(i):
                for index in self.indexes:
                    key = self.values[i][index.id]
                    if len(index.values[key]) == 1:
                        index.values.pop(key)
                    else:
                        index.values[key].remove(i)
                deleted_rows += 1
                del self.values[i]
        if deleted_rows == 1:
            print("{0} row has been deleted".format(deleted_rows))
        else:
            print("{0} rows have been deleted".format(deleted_rows))

    def define(self,left_token, right_token):
        for token in [left_token, right_token]:
            if token.type == "Column":
                if not self.check_columns_presence([token.value]):
                    print('Column name does not match table definition.')
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
                return False
        return True
