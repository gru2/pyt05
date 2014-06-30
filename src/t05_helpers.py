#!/usr/bin/env python2

""" T05 helpers. """

import t05_Object
import t05_Null
import t05_Bool
import t05_Integer
import t05_String
import t05_Node
import t05_CFunction
import t05_Function


tabSize = 4
maxLineLength = 80

class ConvertToString:

    def __init__(self):
        # map obj -> (n_occurances, id)
        self.objData = { }
        self.tabSize = tabSize
        self.maxLineLength = maxLineLength
    
    def toStringNotObject(self, x):
        if x.tag == t05_Null.tag:
            return "null"
        if x.tag == t05_Bool.tag:
            if x.data == True:
                return "true"
            else:
                return "false"
        if x.tag == t05_Integer.tag:
            return str(x.data)
        if x.tag == t05_String.tag:
            return "'" + x.data + "'"
        if x.tag == t05_CFunction.tag:
            return "<cfn " + str(x.data) + ">"
        if x.tag == t05_Function.tag:
            return "<fn " + str(x.data) + ">"
        assert(False)
        return ""

    # Function tryToStringSigleLine does not modify self object.
    def tryToStringSigleLine(self, x, maxLength):
        if x.tag != t05_Object.tag:
            return self.toStringNotObject(x)
        r = ""
        skip = False
        if x in self.objectData:
            data = self.objectData[x]
            r = "*"+str(data[1])

            if data[0] >= 1:
                skip = True
                r = r + "{...}"

        if not skip:
            r = r + "{ "
            for s in x.slots:
                key = self.tryToStringSigleLine(s[0], maxLength - len(r))
                if key == None:
                    return None
                val = self.tryToStringSigleLine(s[1], maxLength - len(r))
                if val == None:
                    return None
                r = r + key + "=" + val + " "
                if len(r) > maxLength:
                    return None
            r = r + "}"
        if len(r) > maxLength:
            return None
        return r

    def toStringSigleLine(self, x):
        if x.tag != t05_Object.tag:
            return self.toStringNotObject(x)
        r = ""
        skip = False
        if x in self.objectData:
            data = self.objectData[x]
            r = "*"+str(data[1])

            if data[0] >= 1:
                skip = True
                r = r + "{...}"

            self.objectData[x] = (data[0] + 1, data[1])

        if not skip:
            r = r + "{ "
            for s in x.slots:
                key = self.toStringSigleLine(s[0])
                val = self.toStringSigleLine(s[1])
                r = r + key + "=" + val + " "
            r = r + "}"
        return r

    def collectObjectData(self, x):
        self.objectIdCount = 0
        self.objectData = { }

        # Recuousively collect all object data.
        self.collectObjectDataRec(x)

        # Remove all objects winth number of occurances <= 1.
        newData = { }
        for obj, data in self.objectData.iteritems():
            if data[0] > 1:
                newData[obj] = (0, self.objectIdCount)
                self.objectIdCount = self.objectIdCount + 1
                print("newdata = " + str(newData[obj]))
        self.objectData = newData

    def collectObjectDataRec(self, x):
        if x.tag != t05_Object.tag:
            return

        if x in self.objectData:
            data = self.objectData[x]
            data = (data[0] + 1, data[1])
            self.objectData[x] = data
            print("data" + str(data))
            return

        self.objectData[x] = (1, -1)

        for s in x.slots:
            self.collectObjectDataRec(s[0])
            self.collectObjectDataRec(s[1])

    def toStringRec(self, x, maxDepth, indent):
        
        if x.tag != t05_Object.tag:
            return self.toStringNotObject(x)

        if maxDepth == 0:
            return "{...}"

        r = self.tryToStringSigleLine(x, self.maxLineLength);
        if r != None:
            return self.toStringSigleLine(x);

        objRef = ""
        skip = False
        if x in self.objectData:
            data = self.objectData[x]
            objRef = "*"+str(data[1])

            if data[0] >= 1:
                skip = True

            self.objectData[x] = (data[0] + 1, data[1])

        r = " " * self.tabSize * indent + objRef + "{\n"

        if skip:
            r = r + " " * self.tabSize * (indent + 1) + "...\n"
            r = r + " " * self.tabSize * indent + "}"
            return r

        for s in x.slots:
            key = self.toStringRec(s[0], maxDepth - 1, indent + 1)
            r = r + " " * self.tabSize * (indent + 1) + key + "="
            val = self.tryToStringSigleLine(s[1], self.maxLineLength);
            if val == None:
                r = r + "\n"                
            val = self.toStringRec(s[1], maxDepth - 1, indent + 1)
            r = r + val + "\n"

        r = r + " " * self.tabSize * indent + "}"

        return r

    def toString(self, x, maxDepth):
        self.collectObjectData(x)
        return self.toStringRec(x, maxDepth, 0)
    
def toString(x, maxDepth = 5):
    cts = ConvertToString()
    return cts.toString(x, maxDepth)


class ConvertNodeToString:
    
    def toString(self, x, skipNextNode = False):
        node = x
        r = ""
        while node != None:
            if node.type == t05_Node.NODE_SELECT:
                r1 = "(<sel>" + self.toString(node.value) + "."
                r1 = r1 + toString(node.literal)
                r = r + r1 + self.argsToString(node) + ")"
            elif node.type == t05_Node.NODE_SLOT:
                r = r + "$" + self.toString(node.value)
            elif node.type == t05_Node.NODE_IDENTIFIER or \
                node.type == t05_Node.NODE_LITERAL:
                if len(node.args) > 0:
                    r = r + ("(") + toString(node.literal)
                    r = r + self.argsToString(node) + ")"
                else:
                    r = r + toString(node.literal)
            elif node.type == t05_Node.NODE_BLOCK:
                r = r + "{ " + self.toString(node.value) + "; }"
                r = r + self.argsToString(node)
            elif node.type == t05_Node.NODE_ARGUMENTS:
                r = r + self.toString(node.value) + "|"
            else:
                r = r + "???"
            if skipNextNode:
                break;
            node = node.next
            if node != None:
                r = r + ";\n"
        return r

    def argsToString(self, x):

        r = ""
        for arg in x.args:
            r = r + " " + self.toString(arg)
        return r

def nodeToString(x, skipNextNode = False):
    cnts = ConvertNodeToString()
    return cnts.toString(x, skipNextNode)
