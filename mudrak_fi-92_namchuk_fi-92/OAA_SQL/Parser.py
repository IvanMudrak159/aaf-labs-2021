import  Database
import re

(CREATE, INDEXED, INSERT, INTO, SELECT, FROM, JOIN, ON, WHERE,
 DELETE) = 'CREATE', 'INDEXED', 'INSERT', 'INTO', 'SELECT', 'FROM', 'JOIN', 'ON', 'WHERE', 'DELETE'

LPAREN, RPAREN, COMMA, LSPAREN, RSPAREN, QUOTES, SEMICOLON = '(', ')', ',', '[', ']', '"', ';'

STRING, EOF = 'STRING', 'EOF'
class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

class Lexer():
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.current_string = None

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        self.pos += 1
        if(self.pos > len(self.text) - 1):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def check_whitespace(self):
        while(self.current_char.isspace()):
            self.advance()

    def get_string(self):
        result = self.current_char
        self.advance()
        while re.match("[a-zA-Z0-9_]", self.current_char) is not None:
            result += self.current_char
            self.advance()
        self.current_string = result

    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.check_whitespace()

            if re.match("[a-zA-Z]", self.current_char) is not None:
                self.get_string()
                if self.current_string.upper() == CREATE:
                    return Token(CREATE, 'CREATE')
                elif self.current_string.upper() == INSERT:
                    return Token(INSERT, 'INSERT')
                elif self.current_string.upper() == DELETE:
                    return Token(INSERT, 'DELETE')
                elif self.current_string.upper() == INDEXED:
                    return Token(INDEXED, 'INDEXED')
                else:
                    return Token(STRING, self.current_string)

            if self.current_char == LPAREN:
                self.advance()
                return Token(LPAREN, '(')
            elif self.current_char == RPAREN:
                self.advance()
                return Token(RPAREN, ')')
            elif self.current_char == COMMA:
                self.advance()
                return Token(COMMA, ',')
            elif self.current_char == LSPAREN:
                self.advance()
                return Token(LSPAREN, '[')
            elif self.current_char == RSPAREN:
                self.advance()
                return Token(RSPAREN, ']')
            elif self.current_char == SEMICOLON:
                self.advance()
                return Token(SEMICOLON, ';')
            elif self.current_char == QUOTES:
                self.advance()
                return Token(QUOTES, '"')
            raise Exception("Unknown symbols")

        return Token(EOF, None)


class Parser():
    def __init__(self, lexer, database):
        self.lexer = lexer
        self.db = database
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor1(self):
        self.eat(STRING)
        if self.current_token.type == INDEXED:
            print("Column has indexed")
            self.eat(INDEXED)

    def create(self):
        self.eat(CREATE)
        table_name = self.current_token.value
        self.eat(STRING)
        self.eat(LPAREN)
        args = []
        args.append(self.current_token.value)
        self.factor1()
        while self.current_token.type != RPAREN:
            self.eat(COMMA)
            args.append(self.current_token.value)
            self.factor1()
        self.eat(RPAREN)
        self.eat(SEMICOLON)


    def factor2(self):
        left_pos = self.lexer.pos
        self.eat(QUOTES)
        while self.current_token.type != QUOTES:
            self.eat(STRING)
        right_pos = self.lexer.pos - 1
        value = self.lexer.text[left_pos : right_pos]
        self.eat(QUOTES)
        return value

    def insert(self):
        self.eat(INSERT)
        if self.current_token.type == INTO:
            self.eat(INTO)
        print('Table name:', self.current_token.value)
        self.eat(STRING)
        self.eat(LPAREN)
        print("Value:",self.factor2())
        while self.current_token.type != RPAREN:
            self.eat(COMMA)
            print("Value:", self.factor2())
        self.eat(RPAREN)
        self.eat(SEMICOLON)

    def delete(self):
        self.eat(DELETE)
        if self.current_token.type == FROM:
            self.eat(FROM)
        print("Table name:",self.current_token.value)
        self.eat(STRING)
        if self.current_token.type == WHERE:
            self.eat(WHERE)

    def parse(self):
        command = self.current_token.type
        if command == CREATE:
            self.create()
        elif command == INSERT:
            self.insert()
        elif command == DELETE:
            self.delete()
        else:
            raise Exception("Invalid syntax")


def main():
    db = Database.Database()
    text = ''
    while True:
        try:
            text += input('> ')
        except EOFError:
            break
        if not text:
            continue
        if ';' not in text:
            text += '\n'
            continue
        lexer = Lexer(text)
        parser = Parser(lexer, db)
        parser.parse()
        text = ''


if __name__ == '__main__':
    main()