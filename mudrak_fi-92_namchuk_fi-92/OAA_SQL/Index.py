from sortedcontainers import SortedDict

class Index:
    def __init__(self, id = 0):
        self.values = SortedDict()
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
        elif operator == '>':
            lines_id = []
            key_list = list(self.values.keys())
            key_pos = key_list.index(value)
            for i in range(key_pos + 1, len(key_list)):
                key = key_list[i]
                for j in range(len(self.values[key])):
                    lines_id.append(self.values[key][j])
            return lines_id
        elif operator == '<':
            lines_id = []
            for i in self.values.keys():
                if i == value:
                    break
                for j in range(len(self.values[i])):
                    lines_id.append(self.values[i][j])
            return lines_id
