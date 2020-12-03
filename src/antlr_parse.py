from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from antlr4.error.Errors import ParseCancellationException
from antlr4.tree.Trees import Trees

from src.antlr.DbQLGrammarLexer import DbQLGrammarLexer
from src.antlr.DbQLGrammarParser import DbQLGrammarParser
from graphviz import Digraph


class TreeAST:
    def __init__(self, input_stream):
        self.tree, self.parser = self.__parse(input_stream)

    class MyErrorListener(ErrorListener):
        def syntaxError(self, recognizer, offending_symbol, line, column, msg, e):
            print(f"Error at {line}:{column}: {msg}; offending symbol: {offending_symbol}")
            raise ParseCancellationException(f"line: {line} msg: {msg}")
    
    def __parse(self, input_stream):
        lexer = DbQLGrammarLexer(input_stream)
        tokens_stream = CommonTokenStream(lexer)
        parser = DbQLGrammarParser(tokens_stream)
        parser.removeErrorListeners()
        parser.addErrorListener(self.MyErrorListener())
        try:
            return parser.script(), parser
        except ParseCancellationException:
            return None, None

    def visualize_tree(self, file):
        if self.tree is not None:
            self.dot = Digraph()
            self.__traverse(self.tree, 0)
            self.dot.render(file, view=True)
        else:
            raise Exception("Parsing tree was failed")

    def __traverse(self, tree, counter):
        root = Trees.getNodeText(tree, DbQLGrammarParser.ruleNames)
        root_name = str(counter)

        for child in Trees.getChildren(tree):
            child_node = Trees.getNodeText(child, DbQLGrammarParser.ruleNames)
            new_counter = counter + 1
            child_name = str(new_counter)
            
            self.dot.node(root_name, root)
            self.dot.node(child_name, child_node)
            self.dot.edge(root_name, child_name)
            
            counter = self.__traverse(child, new_counter)
        
        return counter
