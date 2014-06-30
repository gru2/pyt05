#!/usr/bin/env python2

""" Implementation of T05 parser. """

import t05_Lexer
import t05_Node
import t05_Operator
import t05_SourceCodePosition
import t05_String
import t05_Integer


class Parser:

    def __init__(self):
        self.token = 0
        self.lexer = None
        self.operators = {} # tokenType -> Operator
        self.state = None
        self.errorReporter = None
        self.getSlotLiteral = None
        self.addSlotLiteral = None
        self.setSlotLiteral = None
        self.updateSlotLiteral = None
        self.equalLiteral = None
        self.indexLiteral = None
        self.unaryNegLiteral = None

    def init(self, state):
        assert(self.lexer != None)
        assert(self.lexer.inputStream != None)
        self.state = state
        self.errorReporter = state.errorReporter
        self.lexer.init(state.errorReporter)
        self.operators = {}
        self.lexer.operators = []
        self.lexer.operatorTokens = []
        self.addStandardOperators()
        self.getSlotLiteral = t05_String.new(state, "getSlot")
        self.addSlotLiteral = t05_String.new(state, "addSlot")
        self.setSlotLiteral = t05_String.new(state, "setSlot")
        self.updateSlotLiteral = t05_String.new(state, "updateSlot")
        self.equalLiteral = t05_String.new(state, "=")
        self.indexLiteral = t05_String.new(state, "[]")
        self.unaryNegLiteral = t05_String.new(state, "neg")

    def parseFile(self, fileName):
        if not self.lexer.openInputFile(fileName):
            self.errorReporter.error("unable to open file '" + fileName + "'")
            return
        return self.parse()

    def parseString(self, code, sourceCodePosition):
        self.lexer.openInputString(code, sourceCodePosition)
        return self.parse()
    
    def parse(self):
        self.getNextToken()
        program = self.statements()
        self.postprocess(program)
        return program

    def getNextToken(self):
        self.token = self.lexer.lex()

    def statements(self):
        statements = None
        lastStatement = None
        
        while True:
            if self.token.type == t05_Lexer.TOKEN_EOF:
                break
            if self.token.type == "}":
                break
            s = self.statement()
            if statements == None:
                statements = s
                lastStatement = s
            else:
                lastStatement.next = s
                lastStatement = s
        return statements

    def statement(self):
        token = self.token
        
        if token.type == "$":
            self.getNextToken()
            e = self.expression(t05_Operator.PRECEDENCE_MIN, \
                t05_Operator.ASSOC_LEFT)
            self.expectToken(";")
            return self.makeSlotStatement(e)
        
        if self.isExpression():
            e = self.expression(t05_Operator.PRECEDENCE_MIN, \
                t05_Operator.ASSOC_LEFT)
            self.expectToken(";")
            return e

        return None

    def expression(self, precedence, associativity):
        expr = None
        if self.isLiteral():
            expr = self.makeLiteral()
            self.getNextToken()
        elif self.token.type == t05_Lexer.TOKEN_IDENTIFIER:
            expr = self.makeIdentifier()
            self.getNextToken()
        elif self.token.type == "(":
            self.getNextToken()
            expr = self.expression(t05_Operator.PRECEDENCE_MIN, \
                t05_Operator.ASSOC_LEFT)
            self.expectToken(")")
        elif self.token.type == "{":
            statements = None
            args = None
            scp = t05_SourceCodePosition.SourceCodePosition()
            scp.copy(self.token.sourceCodePosition)
            self.getNextToken()
            if self.isExpression():
                e = self.expression(t05_Operator.PRECEDENCE_MIN, \
                    t05_Operator.ASSOC_LEFT)
                if self.token.type == "|":
                    self.getNextToken()
                    args = e
                    statements = self.statements()
                else:
                    self.expectToken(";")
                    statements = self.statements()
                    e.next = statements
                    statements = e
            else:
                statements = self.statements()
            self.expectToken("}")
            expr = self.makeBlock(args, statements, scp)
        elif self.token.type == "${":
            print("Object literal")
            self.getNextToken()
            objLit = self.expression(t05_Operator.PRECEDENCE_MIN, \
                t05_Operator.ASSOC_LEFT)
            self.expectToken("}")
            expr = self.makeObjectLiteral(objLit)
        elif self.token.type == "-":
            self.getNextToken()
            newPrecedence = t05_Operator.PRECEDENCE_UNARY_NEG
            newAssoc = t05_Operator.ASSOC_LEFT
            scp = t05_SourceCodePosition.SourceCodePosition()
            scp.copy(self.token.sourceCodePosition)
            arg = self.expression(newPrecedence, newAssoc)
            expr = self.makeUnaryOp(self.unaryNegLiteral, arg, scp)
        elif self.token.type == "++":
            self.errorReporter.error("syntax error (expression)")
        elif self.token.type == "--":
            self.errorReporter.error("syntax error (expression)")
        else:
            self.errorReporter.error("syntax error (expression)")

        while True:
            if self.isEndOfExpression(precedence, associativity):
                break
            if self.isBinaryOp():
                lhs = expr
                op = self.operators[self.token.type]
                newPrecedence = op.precedence
                newAssoc = op.associativity
                selector = op.nameAsObject
                scp = t05_SourceCodePosition.SourceCodePosition()
                scp.copy(self.token.sourceCodePosition)
                self.getNextToken()
                rhs = self.expression(newPrecedence, newAssoc)
                if op.tokenType == ".":
                    expr = self.makeSelection(lhs, rhs, scp)
                elif op.tokenType == "=":
                    expr = self.makeAssignment(lhs, rhs, scp)
                else:
                    expr = self.makeBinaryOp(selector, lhs, rhs, scp)
                continue
            if self.isExpression():
                newPrecedence = t05_Operator.PRECEDENCE_GROUP
                newAssoc = t05_Operator.ASSOC_LEFT
                newExpr = self.expression(newPrecedence, newAssoc)
                expr.args.append(newExpr)
                continue
            if self.token.type == "[":
                scp = t05_SourceCodePosition.SourceCodePosition()
                scp.copy(self.token.sourceCodePosition)
                lhs = expr
                selector = self.indexLiteral
                self.getNextToken()
                rhs = self.expression(t05_Operator.PRECEDENCE_MIN, \
                    t05_Operator.ASSOC_LEFT)
                self.expectToken("]")
                expr = self.makeBinaryOp(selector, lhs, rhs, scp)

        return expr

    def makeLiteral(self):
        obj = t05_Node.new(self.state)
        node = t05_Node.get(obj)
        node.type = t05_Node.NODE_LITERAL
        node.literal = self.makeLiteralObject()
        node.sourceCodePosition.copy(self.token.sourceCodePosition)
        return node

    def makeIdentifier(self):
        obj = t05_Node.new(self.state)
        node = t05_Node.get(obj)
        node.type = t05_Node.NODE_IDENTIFIER
        node.literal = t05_String.new(self.state, self.token.value)
        node.sourceCodePosition.copy(self.token.sourceCodePosition)
        return node

    def makeUnaryOp(self, selector, arg, sourceCodePosition):
        obj = t05_Node.new(self.state)
        node = t05_Node.get(obj)
        node.type = t05_Node.NODE_SELECT
        node.value = arg
        node.literal = selector
        node.sourceCodePosition.copy(sourceCodePosition)
        return node

    def makeBinaryOp(self, selector, lhs, rhs, sourceCodePosition):
        obj = t05_Node.new(self.state)
        node = t05_Node.get(obj)
        node.type = t05_Node.NODE_OPERATION
        node.value = lhs
        node.args.append(rhs)
        node.literal = selector
        node.sourceCodePosition.copy(sourceCodePosition)
        return node

    def makeBlock(self, args, statements, sourceCodePosition):
        obj = t05_Node.new(self.state)
        node = t05_Node.get(obj)
        s = statements
        if args != None:
            s = self.makeArguments(args, statements)
        node.type = t05_Node.NODE_BLOCK
        node.value = s
        node.sourceCodePosition.copy(sourceCodePosition)
        return node

    def makeObjectLiteral(self, expr):
        obj = t05_Node.new(self.state)
        node = t05_Node.get(obj)
        node.type = t05_Node.NODE_OBJECT_LITERAL
        node.value = expr
        node.sourceCodePosition.copy(self.token.sourceCodePosition)
        return node

    def makeArguments(self, expr, statements):
        argsObj = t05_Node.new(self.state)
        argsNode = t05_Node.get(argsObj)
        argsNode.type = t05_Node.NODE_ARGUMENTS
        argsNode.value = expr
        argsNode.next = statements
        arg = expr
        
        for newArg in expr.args:
            arg.next = newArg
            arg = newArg
        
        return argsNode 

    def makeSelection(self, lhs, rhs, sourceCodePosition):
        obj = t05_Node.new(self.state)
        node = t05_Node.get(obj)
        if rhs.type != t05_Node.NODE_IDENTIFIER:
            self.errorReporter.error("syntax error - identifier must folow '.'")
        node.type = t05_Node.NODE_SELECT
        node.value = lhs
        node.literal = rhs.literal
        node.sourceCodePosition.copy(sourceCodePosition)
        return node
    
    def makeAssignment(self, lhs, rhs, sourceCodePosition):
        obj = t05_Node.new(self.state)
        node = t05_Node.get(obj)
        node.type = t05_Node.NODE_OPERATION
        node.literal = self.equalLiteral
        node.value = lhs
        node.args.append(rhs)
        node.sourceCodePosition.copy(sourceCodePosition)
        return node

    def makeSlotStatement(self, expr):
        obj = t05_Node.new(self.state)
        node = t05_Node.get(obj)
        node.type = t05_Node.NODE_SLOT;
        node.value = expr
        return node

    def makeLiteralObject(self):
        token = self.token
        if token.type == t05_Lexer.TOKEN_INTEGER:
            return t05_Integer.new(self.state, token.value)
        if token.type == t05_Lexer.TOKEN_STRING:
            return t05_String.new(self.state, token.value)
        self.errorReporter.error("internal error: makeLiteralObject failed")

    def isExpression(self):
        token = self.token
        if token.type == t05_Lexer.TOKEN_IDENTIFIER or self.isLiteral():
            return True
        if token.type == "-" or token.type == "(" or token.type == "{":
            return True
        if token.type == "${":
            return True
        return False

    def isEndOfExpression(self, precedence, associativity):
        token = self.token
        if self.isBinaryOp() or token.type == "[":
            currentOperator = self.operators[token.type]
            newPrecedence = currentOperator.precedence
            if associativity == t05_Operator.ASSOC_LEFT:
                if newPrecedence <= precedence:
                    return True
            else:
                if newPrecedence < precedence:
                    return True
            return False
        if self.isExpression():
            newPrecedence = t05_Operator.PRECEDENCE_GROUP
            if newPrecedence  <= precedence:
                return True
            return False
        return True        

    def isBinaryOp(self):
        token = self.token
        if token.type in ["+", "-", "=", "<", ">", "==", "!=", "*", "/", "%", ".", ","]:
            return True
        return False

    def isLiteral(self):
        if self.token.type in [t05_Lexer.TOKEN_INTEGER, t05_Lexer.TOKEN_DOUBLE, \
            t05_Lexer.TOKEN_STRING]:
            return True
        return False

    def expectToken(self, tokenType):
        if self.token.type != tokenType:
            self.errorReporter.error("syntax error - expected token " + \
                 str(tokenType) + " but found " + str(self.token.type))
        self.getNextToken()

    def postprocess(self, program):
        node = program

        while node != None:
            if node.type == t05_Node.NODE_LITERAL:
                self.postprocessArguments(node)
            elif node.type == t05_Node.NODE_IDENTIFIER:
                self.postprocessArguments(node)
            elif node.type == t05_Node.NODE_SELECT:
                self.postprocessArguments(node)
                self.postprocess(node.value)
            elif node.type == t05_Node.NODE_OPERATION:
                self.postprocessOperation(node)
            elif node.type == t05_Node.NODE_BLOCK:
                self.postprocess(node.value)
            elif node.type == t05_Node.NODE_ARGUMENTS:
                # TBD
                pass
            elif node.type == t05_Node.NODE_SLOT:
                self.postprocessSlot(node)
            elif node.type == t05_Node.NODE_OBJECT_LITERAL:
                #self.postprocess(node.value)
                pass
            else:
                self.errorReporter.error("(t05_Parser)unknown node type:" + str(node.type))
            node = node.next

    def postprocessOperation(self, node):
        if node.literal.equal(self.equalLiteral):
            lhs = node.value
            rhs = node.args[0]
            if lhs.type == t05_Node.NODE_SELECT:
                obj = lhs.value
                node.type = t05_Node.NODE_SELECT
                node.literal = self.updateSlotLiteral
                node.args[0] = lhs
                node.value = obj
                lhs.type = t05_Node.NODE_LITERAL
                lhs.value = None
                node.args.append(rhs)
                self.postprocess(rhs)
                self.postprocess(obj)
            elif lhs.type == t05_Node.NODE_IDENTIFIER:
                node.type = t05_Node.NODE_IDENTIFIER
                node.literal = self.updateSlotLiteral
                node.args[0] = lhs
                lhs.type = t05_Node.NODE_LITERAL
                node.args.append(rhs)
                self.postprocess(rhs)
            elif lhs.type == t05_Node.NODE_OPERATION:
                if lhs.literal.equal(self.indexLiteral):
                    value = rhs
                    obj = lhs.value
                    index = lhs.args[0]
                    node.type = t05_Node.NODE_SELECT
                    node.literal = self.setSlotLiteral
                    node.value = obj
                    node.args[0] = index
                    node.args.append(value)
                    self.postprocess(obj)
                    self.postprocess(index)
                    self.postprocess(value)
                    pass
                else:
                    self.errorReporter.error( \
                        "syntax error - bad lval (operation)")
            else:
                self.errorReporter.error("syntax error - bad lval")
            return
        if node.literal.equal(self.indexLiteral):
            node.type = t05_Node.NODE_SELECT
            node.literal = self.getSlotLiteral
            self.postprocess(node.value)
            self.postprocessArguments(node)
            return

        node.type = t05_Node.NODE_SELECT
        self.postprocess(node.value)
        self.postprocessArguments(node)

    def postprocessArguments(self, node):
       for arg in node.args:
            self.postprocess(arg)

    def postprocessSlot(self, node):
        value = None
        expr = node.value

        if expr.type == t05_Node.NODE_IDENTIFIER:
            key = expr
            node.type = t05_Node.NODE_IDENTIFIER
            node.value = None
            node.args.append(key)
            node.literal = self.addSlotLiteral
            key.type = t05_Node.NODE_LITERAL
        elif expr.type == t05_Node.NODE_SELECT:
            key = node.value
            obj = key.value
            node.type = t05_Node.NODE_SELECT
            node.literal = self.addSlotLiteral
            node.value = obj
            node.args.append(key)
            key.type = t05_Node.NODE_LITERAL
        elif expr.type == t05_Node.NODE_OPERATION:
            key = expr.value
            if key.type == t05_Node.NODE_IDENTIFIER:
                node.type = t05_Node.NODE_IDENTIFIER
                node.value = None
                node.args.append(key)
                node.literal = self.addSlotLiteral
                key.type = t05_Node.NODE_LITERAL
                value = expr.args[0]
            elif key.type == t05_Node.NODE_SELECT:
                node.type = t05_Node.NODE_SELECT
                node.value = key.value
                key.value = None
                node.args.append(key)
                node.literal = self.addSlotLiteral
                key.type = t05_Node.NODE_LITERAL
                value = expr.args[0]
        if value == None:
            valueObj = t05_Node.new(self.state)
            value = t05_Node.get(valueObj)
            value.type = t05_Node.NODE_LITERAL
            value.literal = self.state.protos.null
        node.args.append(value)
        self.postprocess(node)

    def addOperator(self, opName, tokenType, precedence, associativity, position):
        op = t05_Operator.Operator()
        op.setName(opName, self.state)
        op.tokenType = tokenType
        op.precedence = precedence
        op.associativity = associativity
        op.position = position
        self.operators[tokenType] = op
        self.lexer.operators.append(opName)
        self.lexer.operatorTokens.append(tokenType)

    def addStandardOperators(self):
        delimiter = t05_Operator.POSITION_DELIMITER
        infix = t05_Operator.POSITION_INFIX
        prefix = t05_Operator.POSITION_PREFIX
        left = t05_Operator.ASSOC_LEFT
        right = t05_Operator.ASSOC_RIGHT
        add_sub = t05_Operator.PRECEDENCE_ADD_SUB
        mul_div = t05_Operator.PRECEDENCE_MUL_DIV
        min_ = t05_Operator.PRECEDENCE_MIN
        dot = t05_Operator.PRECEDENCE_DOT
        compare = t05_Operator.PRECEDENCE_COMPARE
        assignment = t05_Operator.PRECEDENCE_ASSIGNMENT
        index = t05_Operator.PRECEDENCE_INDEX
        slot = t05_Operator.PRECEDENCE_SLOT
        comma = t05_Operator.PRECEDENCE_COMMA
        self.addOperator(";", ";", 0, 0, delimiter)
        self.addOperator("|", "|", 0, 0, delimiter)
        self.addOperator("+", "+", add_sub, left, infix)
        self.addOperator("-", "-", add_sub, left, infix)
        self.addOperator("*", "*", mul_div, left, infix)
        self.addOperator("(", "(", min_, left, delimiter)
        self.addOperator(")", ")", min_, left, delimiter)
        self.addOperator("{", "{", min_, left, delimiter)
        self.addOperator("}", "}", min_, left, delimiter)
        self.addOperator(".", ".", dot, left, infix)
        self.addOperator("<", "<", compare, left, infix)
        self.addOperator(">", ">", compare, left, infix)
        self.addOperator("==", "==", compare, left, infix)
        self.addOperator("!=", "!=", compare, left, infix)
        self.addOperator("=", "=", assignment, right, infix)
        self.addOperator("[", "[", index, left, infix)
        self.addOperator("]", "]", index, left, infix)
        self.addOperator("${", "${", min_, left, delimiter)
        self.addOperator("$", "$", slot, left, prefix)
        self.addOperator(",", ",", comma, left, infix)
