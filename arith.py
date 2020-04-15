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


INT, SUM, SUB, MUL, EOF = ['INTEGER', 'SUM', 'SUB', 'MUL', 'EOF']

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
    
# Operand Node Class for AST
class Operand_Node(AST):
    def __init__(self, token):
        self.value = token.value
       
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
            
    # Read whole number
    def get_int(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)
        
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
            
            raise Exception('Syntax Error...')
            
        return Token(EOF, None)
    
class Parser(object):
    def __init__(self,lexer):
        self.lexer = lexer

        self.current_token = self.lexer.get_next_token()

        
    def _get_next_token(self):
        self.current_token = self.lexer.get_next_token()
        
    def factor(self):          
        if self.current_token.type == INT:
            token = self.current_token
            self._get_next_token()
            return Operand_Node(token)
        
    def term(self):
        node = self.factor()     
        while self.current_token.type is MUL:
            token = self.current_token
            self._get_next_token()
            node = Operator_Node(left=node, operation=token, right=self.factor())
        return node
    
    def expression(self):      
        node = self.term()
        while self.current_token.type in [SUM, SUB]:
            token = self.current_token
            self._get_next_token()
            node = Operator_Node(left=node, operation=token, right=self.term())  
        return node 
    
    def parse(self):
        return self.expression()
    
class Interpreter(object):
    def __init__(self):
        pass
        
    def visit(self, node):
        
        if type(node) == Operand_Node:
            return self.visit_operand(node)
            
        elif type(node) == Operator_Node:
            return self.visit_operator(node)
        
    def visit_operand(self, node):
        return node.value
        
    def visit_operator(self, node):
        if node.operation.type == SUM:
            return self.visit(node.left) + self.visit(node.right)
        
        elif node.operation.type == SUB:
            return self.visit(node.left) - self.visit(node.right)
        
        elif node.operation.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        
        
            
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
        result = interpreter.eval(AST)
        print(result)
    
if __name__ == '__main__':
    main()

