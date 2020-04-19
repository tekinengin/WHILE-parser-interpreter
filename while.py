#!/usr/bin/env python
# coding: utf-8

# Author Engin Tekin github.com/tekinengin
'''
This script typed for CSE210A-Programming Languages - Semantic Applications

@Following tutorial has been used during preparation of this code. --- #### https://ruslanspivak.com/lsbasi-part7/ ####

There are four main classes AST, LEXER, PARSER, INTERPRETER

AST: Base Class in order to store Abstract-Syntax Tree

LEXER: This class is created to pass through input and tokenize components.

PARSER: Parser is using tokenized input in order to create Abstract-Syntax Tree (AST)

INTERPRETER: This class accepts an AST and evaluate it.

'''


INT, BOOLEAN, SUM, SUB, MUL, AND, OR, NOT, EQ, LESS, LPARENT, RPARENT, ASSIGN, ID, SEMCOL, SKIP, LSCOPE, RSCOPE, IF, THEN, ELSE, WHILE, DO, EOF = \
        ['INTEGER', 'BOOLEAN', 'SUM', 'SUB', 'MUL', 'AND', 'OR', 'NOT', 'EQ', 'LESS', '(', ')', ':=', 'ID', ';', 'SKIP', '{', '}', 'IF', 'THEN', 'ELSE', 'WHILE', 'DO','EOF']

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value
        
# Base Class for AST Data Structure
class AST:
    pass

# Operator Node Class for AST
class Operator_Node(AST):
    def __init__(self, left, operation, right):
        self.left = left
        self.operation = operation
        self.right = right
    
# Uni-Operator Node Class for AST
class Uni_Operator_Node(AST):
    def __init__(self, operation, expr):
        self.operation = operation
        self.expr = expr

# Operand Node Class for AST
class Operand_Node(AST):
    def __init__(self, token):
        self.type = token.type
        self.value = token.value

# Assign Node Class for AST
class Assign_Node(AST):
    def __init__(self, var, operation, expr):
        self.var = var
        self.operation = operation
        self.expr = expr

# Variable Node Class for AST
class Var_Node(AST):
    def __init__(self, token):
        self.token = token
        self.id = token.value

class Pass_Node(AST):
    pass

class Scope_Node(AST):
    def __init__(self):
        self.statement_list = []

class If_Node(AST):
    def __init__(self, condition, then_scope, else_scope):
        self.condition = condition
        self.then_scope = then_scope
        self.else_scope = else_scope

class While_Node(AST):
    def __init__(self,condition, scope):
        self.condition = condition
        self.scope = scope
       
# Lexer Class in order to tokenize input 
class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.current_pos = 0
        self.current_char = text[self.current_pos]
       
    # Mode Cursor until EOF 
    def advance(self):
        self.current_pos += 1
        
        if self.current_pos == len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.current_pos]

    def check_next(self):
        pos = self.current_pos + 1
        
        if pos == len(self.text):
            return None
        else:
            return self.text[pos]

            
    # Read whole number
    def get_int(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    # Read word
    def get_word(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        return result

        
    # Reads next token
    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.advance()
                continue
                
            # '-' can be before a negative number or can be a operator 
            elif self.current_char == '-':
                self.advance()
                if self.current_char.isspace():
                    return Token(SUB, '-')
                else:
                    return Token(INT, -1 * self.get_int())
                
            elif self.current_char.isdigit():
                return Token(INT, self.get_int())
            
            elif self.current_char == '+':
                self.advance()
                return Token(SUM, '+')
            
            elif self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            elif self.current_char == '(':
                self.advance()
                return Token(LPARENT, '(')

            elif self.current_char == ')':
                self.advance()
                return Token(RPARENT, ')')

            elif self.current_char == '∧':
                self.advance()
                return Token(AND, 'and')

            elif self.current_char == '∨':
                self.advance()
                return Token(OR, 'or')

            elif self.current_char.isalpha():
                word = self.get_word()
                if word == 'true':
                    return Token(BOOLEAN, True)
                elif word == 'false':
                    return Token(BOOLEAN, False)
                elif word == 'skip':
                    return Token(SKIP, 'pass') # ????
                elif word == 'if':
                    return Token(IF, 'IF')
                elif word == 'then':
                    return Token(THEN, 'THEN')
                elif word == 'else':
                    return Token(ELSE, 'ELSE')
                elif word == 'while':
                    return Token(WHILE, 'WHILE')
                elif word == 'do':
                    return Token(DO, 'do')
                else:
                    return Token(ID, word)

            elif self.current_char == '{':
                return Token(LSCOPE, '{')

            elif self.current_char == '}':
                return Token(RSCOPE, '}')


            elif self.current_char == '¬':
                self.advance()
                return Token(NOT,'¬')

            elif self.current_char == '=':
                self.advance()
                return Token(EQ,'=')

            elif self.current_char == '<':
                self.advance()
                return Token(LESS,'<')

            elif self.current_char == ':' and self.check_next() == '=':
                self.advance()
                self.advance()
                return Token(ASSIGN, ':=')

            elif self.current_char == ';':
                self.advance()
                return Token(SEMCOL, ';')



            print(self.current_char)


            
            raise Exception('Syntax Error...')
            
        return Token(EOF, None)
    
class Parser(object):
    def __init__(self,lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

        
    def _get_next_token(self):
        self.current_token = self.lexer.get_next_token()

    def if_statement(self):
        condition = self.expression()
        self._get_next_token() ## skip 'then' token
        then_scope = self.scope_statement()
        self._get_next_token() ## skip 'else' token
        else_scope = self.scope_statement()
        return If_Node(condition, then_scope, else_scope)

    def while_statement(self):
        condition = self.expression()
        self._get_next_token() ## Skip 'do' token
        scope = self.scope_statement()
        return While_Node(condition, scope)
        
    def scope_statement(self):
        nodes = self.statement_list()
        
        root = Scope_Node()
        for node in nodes:
            root.statement_list.append(node)

        return root
        
    def statement_list(self):
        node = self.statement()
        scope = [node]

        while self.current_token.type == SEMCOL:
            self._get_next_token()
            scope.append(self.statement())

        return scope
        
    def statement(self):
        if self.current_token.type == ID:
            node = self.assignment_statement()
        elif self.current_token.type == SKIP:
            node = Pass_Node()
        elif self.current_token.type == IF:
            self._get_next_token()
            node = self.if_statement()
        elif self.current_token.type == WHILE:
            self._get_next_token()
            node = self.while_statement()
        return node

    def assignment_statement(self):
        left = self.variable()
        token = self.current_token
        self._get_next_token()
        right = self.expression()
        node = Assign_Node(left, token, right)
        return node

    def variable(self):
        node = Var_Node(self.current_token)
        self._get_next_token()
        return node
        
    def factor(self):         
        if self.current_token.type in [INT, BOOLEAN]:
            token = self.current_token
            self._get_next_token()
            return Operand_Node(token)

        elif self.current_token.type == NOT:
            token = self.current_token
            self._get_next_token()
            node = Uni_Operator_Node(operation=token, expr= self.factor())
            return node

        elif self.current_token.type == LPARENT:
            self._get_next_token()
            node = self.expression()
            self._get_next_token()
            return node

        else:
            node = self.variable()
            return node

        
    def term(self):
        node = self.factor()     
        while self.current_token.type is MUL:
            token = self.current_token
            self._get_next_token()
            node = Operator_Node(left=node, operation=token, right=self.factor())
        return node
    
    def expression(self):      
        node = self.term()
        while self.current_token.type in [SUM, SUB, AND, OR, EQ, LESS]:
            token = self.current_token
            self._get_next_token()
            node = Operator_Node(left=node, operation=token, right=self.term())  
        return node 
    
    def parse(self):
        return self.scope_statement()
    
class Interpreter(object):
    def __init__(self):
        self.GLOBAL_SCOPE = {}
        
    def visit(self, node):
        if type(node) == Scope_Node:
            return self.visit_Scope(node)
        
        elif type(node) == Assign_Node:
            return self.visit_Assign(node)
        
        elif type(node) == Var_Node:
            return self.visit_Var(node)
        
        elif type(node) == Pass_Node:
            return self.visit_Pass(node)
        
        elif type(node) == Operand_Node:
            return self.visit_operand(node)
            
        elif type(node) in [Operator_Node, Uni_Operator_Node]:
            return self.visit_operator(node)
        
        elif type(node) == If_Node:
            return self.visit_If(node)
        
        elif type(node) == While_Node:
            return self.visit_While(node)
        
    def visit_operand(self, node):
        return node.value
        
    def visit_operator(self, node):
        if node.operation.type == SUM:
            return self.visit(node.left) + self.visit(node.right)
        
        elif node.operation.type == SUB:
            return self.visit(node.left) - self.visit(node.right)
        
        elif node.operation.type == MUL:
            return self.visit(node.left) * self.visit(node.right)

        elif node.operation.type == AND:
            return self.visit(node.left) and self.visit(node.right)

        elif node.operation.type == OR:
            return self.visit(node.left) or self.visit(node.right)

        elif node.operation.type == EQ:
            return self.visit(node.left) == self.visit(node.right)

        elif node.operation.type == LESS:
            return self.visit(node.left) < self.visit(node.right)

        elif node.operation.type == NOT:
            return not (self.visit(node.expr))
        
        
    def visit_Assign(self,node):
        var_name = node.var.id
        self.GLOBAL_SCOPE[var_name] = self.visit(node.expr)
        
    def visit_Var(self, node):
        var_name = node.id
        value = self.GLOBAL_SCOPE.get(var_name)
        if value is None:
            return 0 ## Assuming every variable is INTEGER
        return value

    def visit_Pass(self, node):
        pass
    
    def visit_Scope(self, node):
        for statement in node.statement_list:
            self.visit(statement)
    
    def visit_If(self, node):
        if self.visit(node.condition):
            return self.visit(node.then_scope)
        else:
            return self.visit(node.else_scope)

    def visit_While(self, node):
        while self.visit(node.condition):
            self.visit(node.scope)

    def eval(self, root):
        return self.visit(root)


def main():
    while True:
        try:
            try:
                text = raw_input('')
            except NameError:  # Python3
                text = input('')
        except EOFError:
            break
        if not text:
            continue

        lexer = Lexer(text)
        parser = Parser(lexer)
        AST = parser.parse()
        interpreter = Interpreter()
        interpreter.eval(AST)
        keys = list(interpreter.GLOBAL_SCOPE.keys())
        len_keys = len(keys)
        result = '{'
        for index in range(len_keys):
            result += keys[index] + ' → ' + str(interpreter.GLOBAL_SCOPE[keys[index]])
            if len_keys - index - 1 > 0:
                result += ', '
    
        result += '}'
        print(result)
    
if __name__ == '__main__':
    main()