'''
Created on Jun 25, 2012

To get the input from the XML File using xml.sax

@author: Gaylord Cherencey
'''
from xml.sax import handler

class MySaxDocumentHandler(handler.ContentHandler):
    '''Class which go through the XML file a extract the input'''

    def __init__(self):
        self.level = 0
        self.inInput = False
        self.inputsList = []

    def get_inputsList(self):
        return self.inputsList

    def startDocument(self):
        pass

    def endDocument(self):
        pass

    def startElement(self, name, attrs):

        #we go through the tags into the XML File
        #we get name attribute if we find this layout:
        #<input>
        #    <file  name="">

        self.level += 1

        if name == 'input':
            self.inInput = True

        elif self.inInput and name == 'file':
            for attrName in attrs.keys():
                if attrName == 'name':
                    self.inputsList.append(attrs.get(attrName))

    def endElement(self, name):
        if name == 'input':
            self.inInput = False

        self.level -= 1