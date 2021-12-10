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

        keys_list = list(self.values.keys())
        mid = len(keys_list) // 2
        low = 0
        high = len(keys_list) - 1
        while keys_list[mid] != value and low <= high:
            if value > keys_list[mid]:
                low = mid + 1
            else:
                high = mid - 1
            mid = (low + high) // 2

        if operator == '>' or operator == '>=':
            lines_id = []
            key_pos = mid + 1
            if operator == '>=':
                key_pos -= 1
            for i in range(key_pos, len(keys_list)):
                key = keys_list[i]
                for j in range(len(self.values[key])):
                    lines_id.append(self.values[key][j])
            return lines_id
        elif operator == '<' or operator == '<=':
            lines_id = []
            key_pos = mid
            if operator == '<=':
                key_pos += 1
            for i in range(0, key_pos):
                key = keys_list[i]
                for j in range(len(self.values[key])):
                    lines_id.append(self.values[key][j])
            return lines_id