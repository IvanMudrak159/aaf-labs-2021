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
        print('index')
        if operator == '=':
            lines_id = self.values.get(value)
            if lines_id:
                return lines_id
            return []
        elif operator == '>':
            lines_id = []
            is_bigger = False
            for i in self.values.keys():
                if is_bigger:
                    for j in range(len(self.values[i])):
                        lines_id.append(self.values[i][j])
                if i == value:
                    is_bigger = True
            if lines_id is None:
                return []
            return lines_id
        elif operator == '<':
            lines_id = []
            for i in self.values.keys():
                if i == value:
                    return lines_id
                for j in range(len(self.values[i])):
                    lines_id.append(self.values[i][j])
            if lines_id is None:
                return []
            return lines_id
        elif operator == '!=':
            lines_id = []
            for i in self.values.keys():
                if i == value:
                    continue
                for j in range(len(self.values[i])):
                    lines_id.append(self.values[i][j])
            if lines_id is None:
                return []
            return lines_id
