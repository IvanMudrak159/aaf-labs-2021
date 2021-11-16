import Database
import re

(CREATE, INDEXED, INSERT, INTO, SELECT, FROM, JOIN, ON, WHERE,
 DELETE, EXIT) = 'CREATE', 'INDEXED', 'INSERT', 'INTO', 'SELECT', 'FROM', 'JOIN', 'ON', 'WHERE', 'DELETE', 'EXIT'

LPAREN, RPAREN, COMMA, LSPAREN, RSPAREN, QUOTES, ASTERISK, SEMICOLON = '(', ')', ',', '[', ']', '"', '*', ';'
EQUALS, GREATER, LESS, EXCLAMATION = '=', '>', '<', '!'
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
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def check_whitespace(self):
        while(self.current_char.isspace()):
            self.advance()

    def get_word(self):
        result = self.current_char
        self.advance()
        while re.match("[a-zA-Z0-9_]", self.current_char) is not None:
            result += self.current_char
            self.advance()
        self.current_string = result

    def get_string(self):
        result = ''
        while self.current_char != QUOTES:
            if type(self.current_char).__name__ == 'str':
                result += self.current_char
                self.advance()
            else:
                return False
        self.current_string = result
        return True

    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.check_whitespace()

            if re.match("[a-zA-Z]", self.current_char) is not None:
                self.get_word()
                if self.current_string.upper() == CREATE:
                    return Token(CREATE, 'CREATE')
                elif self.current_string.upper() == INSERT:
                    return Token(INSERT, 'INSERT')
                elif self.current_string.upper() == SELECT:
                    return Token(SELECT, 'SELECT')
                elif self.current_string.upper() == WHERE:
                    return Token(WHERE, 'WHERE')
                elif self.current_string.upper() == DELETE:
                    return Token(DELETE, 'DELETE')
                elif self.current_string.upper() == INDEXED:
                    return Token(INDEXED, 'INDEXED')
                elif self.current_string.upper() == INTO:
                    return Token(INTO, 'INTO')
                elif self.current_string.upper() == FROM:
                    return Token(FROM, 'FROM')
                elif self.current_string.upper() == EXIT:
                    return Token(EXIT, 'EXIT')
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
            elif self.current_char == ASTERISK:
                self.advance()
                return Token(STRING, '*')
            elif self.current_char == EQUALS:
                self.advance()
                return Token(EQUALS, '=')
            elif self.current_char == GREATER:
                self.advance()
                return Token(GREATER, '>')
            elif self.current_char == LESS:
                self.advance()
                return Token(LESS, '<')
            elif self.current_char == EXCLAMATION:
                self.advance()
                return Token(EXCLAMATION, '!')
            break

        return Token(EOF, None)


class Parser():
    def __init__(self, lexer, database):
        self.lexer = lexer
        self.db = database
        self.current_token = self.lexer.get_next_token()

    def error(self):
        input_text(self.db)

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            print('Invalid syntax')
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
        value = [self.current_token.value]
        args.append(value)
        self.factor1()
        while self.current_token.type != RPAREN:
            self.eat(COMMA)
            value = [self.current_token.value]
            args.append(value)
            self.factor1()
        self.eat(RPAREN)
        self.eat(SEMICOLON)

        self.db.create(table_name, args)

    def factor2(self):
        left_pos = self.lexer.pos
        self.lexer.advance()
        if not self.lexer.get_string():
            print("Invalid syntax. Expected string")
            self.error()
        right_pos = self.lexer.pos
        value = self.lexer.text[left_pos: right_pos]
        self.lexer.advance()
        self.eat(QUOTES)
        return value

    def insert(self):
        self.eat(INSERT)
        if self.current_token.type == INTO:
            self.eat(INTO)
        table_name = self.current_token.value
        self.eat(STRING)
        self.eat(LPAREN)
        args = []
        args.append(self.factor2())
        while self.current_token.type != RPAREN:
            self.eat(COMMA)
            args.append(self.factor2())
        self.eat(RPAREN)
        self.eat(SEMICOLON)

        self.db.insert(table_name, args)

    def factor3(self):
        result = ''
        while self.current_token.type != QUOTES and self.current_token.type != EOF:
            result += self.current_token.value
            self.eat(self.current_token.type)
        if result in ('=', '!=', '>', '<', '>=', '<='):
            return result
        else:
            print("Invalid syntax. Incorrect operator.")

    def select(self):
        self.eat(SELECT)
        columns = []
        while self.current_token.type != FROM:
            if self.current_token.type == COMMA:
                self.eat(COMMA)
            columns.append(self.current_token.value)
            self.eat(STRING)
        self.eat(FROM)
        table_name = self.current_token.value
        self.eat(STRING)
        if self.current_token.type == WHERE:
            self.eat(WHERE)
            column_name = [self.current_token.value]
            self.eat(STRING)
            operator = self.factor3()
            value = self.factor2().strip()
            self.eat(SEMICOLON)
            self.db.select(table_name, columns, column_name, operator, value)
        else:
            self.eat(SEMICOLON)
            self.db.select(table_name, columns)

    def delete(self):
        self.eat(DELETE)
        if self.current_token.type == FROM:
            self.eat(FROM)
        table_name = self.current_token.value
        self.eat(STRING)
        if self.current_token.type == WHERE:
            self.eat(WHERE)

    def parse(self):
        command = self.current_token.type
        if command == CREATE:
            self.create()
        elif command == INSERT:
            self.insert()
        elif command == SELECT:
            self.select()
        elif command == DELETE:
            self.delete()
        elif command == EXIT:
            SystemExit()
        else:
            print("Invalid syntax")


class CLI:
    def __init__(self, db):
        self.db = db

    def run(self):
        input_text(self.db)


def input_text(db):
    text = ''
    while True:
        try:
            text += input('> ')
        except EOFError:
            break
        if not text:
            continue
        if text.upper() == 'EXIT':
            exit()
        if ';' not in text:
            text += '\n'
            continue
        lexer = Lexer(text)
        parser = Parser(lexer, db)
        parser.parse()
        text = ''
