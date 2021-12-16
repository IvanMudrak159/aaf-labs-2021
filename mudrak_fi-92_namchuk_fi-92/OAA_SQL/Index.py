import sortedcontainers

class Index:
    def __init__(self, id = 0):
        self.values = sortedcontainers.SortedDict()
        self.id = id

    def insert(self, column_value, lines_id):
        if self.values.get(column_value):
            self.values[column_value].append(lines_id)
        else:
            self.values[column_value] = [lines_id]

    def get_lines(self, operator, value):
        if operator == '=':
            lines_id = self.values.get(value)
            if lines_id:
                return lines_id
            return []

        keys_list = sortedcontainers.SortedList(list(self.values.keys()))
        key_pos = keys_list.bisect_left(value)

        if operator == '>' or operator == '>=':
            lines_id = []
            if self.values.get(value) is not None and operator == '>':
                key_pos += 1
            for i in range(key_pos, len(keys_list)):
                key = keys_list[i]
                for j in range(len(self.values[key])):
                    lines_id.append(self.values[key][j])
            return lines_id
        elif operator == '<' or operator == '<=':
            lines_id = []
            if self.values.get(value) is not None and operator == '<=':
                key_pos += 1
            for i in range(0, key_pos):
                key = keys_list[i]
                for j in range(len(self.values[key])):
                    lines_id.append(self.values[key][j])
            return lines_id
