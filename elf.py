#! /usr/bin/python
# coding=utf-8

import sys
import re

ItemStart = r' <1>'
MemberStart = r' <2>'

NamePattern = re.compile(r'^\s*<\w+>\s+DW_AT_name.+:\s+(\w+)\s*$')
TypePattern = re.compile(r'^\s*<\w+>\s+DW_AT_type.+:\s+<0x(\w+)>\s*$')
ArrayBoundPattern = re.compile(r'^\s*<\w+>\s+DW_AT_upper_bound.+:\s+(\d+)\s*$')
BitSizePattern = re.compile(r'^\s*<\w+>\s+DW_AT_bit_size.+:\s+(\d+)\s*$')


class SourceParser():
    ""

    def _next(self, source, tag):
        first = True
        itemBegin = False
        last = ''
        item = []
        for line in source:
            if line.startswith(tag):
                if first:
                    first = False
                else:
                    if last: item.insert(0, last)
                    yield item
                    item = []
                itemBegin = True
                last = line
            else:
                if itemBegin:
                    item.append(line)

    def _nextItem(self, source):
        for item in self._next(source, ItemStart):
            yield item

    def _nextNember(self, source):
        for item in self._next(source, MemberStart):
            yield item

    def _generateItem(self, item):
        pos = item[0].rfind('(')
        itemType = item[0][pos+1 : -2]

        try:
            func = getattr(self, 'do'+itemType)
            return func(item)
        except AttributeError:
            print 'This Type: "%s" Can\'t Parse!' % itemType
            print ''.join(item)
            return None

    def _generateMember(self, member):
        if len(member) == 6:
            return self.doCommonMember(member)
        elif len(member) == 9:
            return self.doBitMember(member)
        else:
            print 'This Member Can\'t Parse:\n%s' % ''.join(member)
            return None

    def doDW_TAG_base_type(self, source):
        return BaseType(source)

    def doDW_TAG_structure_type(self, source):
        struct = StructType(source)
        for member in self._nextNember(source):
            mem = self._generateMember(member)
            if mem:
                struct.addMember(self._generateMember(member))
            else:
                return None

        return struct

    def doDW_TAG_typedef(self, source):
        return TypeDef(source)

    def doDW_TAG_array_type(self, source):
        return ArrayType(source)

    def doDW_TAG_pointer_type(self, source):
        return PointerType(source)

    def doCommonMember(self, source):
        return CommomMember(source)

    def doBitMember(self, source):
        return BitMember(source)

    def parse(self, f):
        for item in self._nextItem(f):
            obj = self._generateItem(item)
            if obj: yield obj

class Item(object):
    def __init__(self, source):
        self._parse(source)

    def _parse(self, source):
        pass

    def getId(self, source):
        return source[0].split('>')[1][1:]

    #def getName(self, s):
    #    return s.rsplit(':')[-1].strip()
    def getName(self, source):
        name = self._search(source, NamePattern)
        return name

    #def getType(self, s):
    #    return s.rsplit(':')[-1].strip()[3:-1]

    def getType(self, source):
        type = self._search(source, TypePattern)
        return type

    def _search(self, source, pattern):
        for s in source:
            r = pattern.match(s)
            if r:
                return r.group(1)

class BaseType(Item):
    def __init__(self, source):
        super(BaseType, self).__init__(source)

    def _parse(self, source):
        self.id = self.getId(source)
        self.name = self.getName(source)

    def format(self):
        return '%s|%s' % (self.id, self.name)

    def construction(self, name='', dict={}):
        return self.name + ' ' + name

class TypeDef(Item):
    def __init__(self, source):
        super(TypeDef, self).__init__(source)

    def _parse(self, source):
        self.id = self.getId(source)
        self.name = self.getName(source)
        self.type = self.getType(source)

    def format(self):
        return '%s|%s|%s' % (self.id, self.name, self.type)

    def isStruct(self, dict):
        return isinstance(dict[self.type], StructType)

    def construction(self, name='', dict={}):
        if self.isStruct(dict):
            return dict[self.type].construction('', dict)
        else:
            return self.name + ' ' + name

class ArrayType(Item):
    def __init__(self, source):
        super(ArrayType, self).__init__(source)

    def _parse(self, source):
        self.id = self.getId(source)
        self.type = self.getType(source)
        self.len = self.getLen(source)

    #def getLen(self, s):
    #    return s.rsplit(':')[-1].strip()

    def getLen(self, source):
        len = self._search(source, ArrayBoundPattern)
        print 'Len: %s, %s' % (len, source)
        return len

    def format(self):
        return '%s|%s|%s' % (self.id, self.type, self.len)

    def construction(self, name, dict={}):
        obj = dict[self.type]
        return obj.name + ' ' + name + '[' + str(int(self.len) + 1) + ']'

class PointerType(Item):
    def __init__(self, source):
        super(PointerType, self).__init__(source)

    def _parse(self, source):
        self.id = self.getId(source)
        self.type = self.getType(source)

    def format(self):
        return '%s|%s' % (self.id, self.type)

    def construction(self, name, dict={}):
        obj = dict[self.type]
        return obj.name + '*' + ' ' + name

class StructMember(Item):
    def __init__(self, source):
        super(StructMember, self).__init__(source)

    def _parse(self, source):
        self.name = self.getName(source)
        self.type = self.getType(source)

class CommomMember(StructMember):
    def __init__(self, source):
        super(CommomMember, self).__init__(source)

    def format(self):
        return '%s %s' % (self.type, self.name)

    def construction(self, name='', dict={}):
        obj = dict[self.type]
        if isinstance(obj, TypeDef):
            return obj.name + ' ' + self.name
        else:
            return obj.construction(self.name, dict)

class BitMember(StructMember):
    def __init__(self, source):
        super(BitMember, self).__init__(source)
        self.len = self.getLen(source)

    #def getLen(self, s):
    #    return s.rsplit(':')[-1].strip()

    def getLen(self, source):
        len = self._search(source, BitSizePattern)
        print 'Len: %s, %s' % (len, source)
        return len

    def format(self):
        return '%s %s:%s' % (self.type, self.name, self.len)

    def construction(self, name='', dict={}):
        obj = dict[self.type]
        return obj.name + ' ' + self.name + ':' + self.len

class StructType(Item):
    def __init__(self, source):
        self.member = []
        super(StructType, self).__init__(source)

    def _parse(self, source):
        self.id = self.getId(source)
        self.name = self.getName(source)

    def addMember(self, member):
        self.member.append(member)

    def format(self):
        return '%s|%s|%s' % (self.id, self.name,
                ';'.join([member.format() for member in self.member]))

    def construction(self, name='', dict={}):
        result = []
        for member in self.member:
            result.append(member.construction('', dict))

        return ';'.join(result)


if __name__ == '__main__':

    if len(sys.argv) > 1:
        f = open(sys.argv[1])
    else:
        f = sys.stdin
    source = SourceParser()
    items = {}
    for item in source.parse(f):
        items[item.id] = item
    print 'Total Items: %d' % len(items)

    #for item in items.values():
    #    print item.format()

    #for item in items.values():
    #    if isinstance(item, StructType):
    #        print item.name, '|', item.construction(dict = items)

    for item in items.values():
        try:
            if isinstance(item, TypeDef) and item.isStruct(items):
                print item.name, '|', item.construction(dict = items)
        except KeyError:
            pass


