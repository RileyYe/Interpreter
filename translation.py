#! /usr/bin/env python
# coding=utf-8
from __future__ import division, print_function
from node import *


class Class:
    def __init__(self, v_table):
        self.v_table = v_table


f_table = {}
class_table = {}


class Translate:

    def __init__(self):
        self.v_table = {}
        self.loop_break_registration = []

    def parse_aggregation_to_list(self, node):
        if len(node.getchildren()) == 1:
            if node.getchild(0).getdata().isdigit():  # 如果是数字
                return [int(node.getchild(0).getdata())]  # 就返回数字
            else:
                return [node.getchild(0).getdata()]  # 否则查找v_table，返回v_table中的变量值
        else:
            if node.getchild(0).getdata().isdigit():  # 如果是数字
                return [int(node.getchild(0).getdata())] + self.parse_aggregation_to_list(node.getchild(1))  # 就返回数字
            else:
                return [node.getchild(0).getdata()] + self.parse_aggregation_to_list(
                    node.getchild(1))  #

    def update_v_table(self, name, value):
        self.v_table[name] = value

    def trans(self, node):

        if len(self.loop_break_registration) > 0:
            if not self.loop_break_registration[-1]:
                return
        # Assignment
        if node.getdata() == '[ASSIGNMENT]':
            def recursively_calculate_rvalue(node):
                if len(node.getchildren()) == 1:  # 触碰到递归边界
                    if node.getchild(0).getdata().isdigit():  # 如果是数字
                        return int(node.getchild(0).getdata())  # 就返回数字
                    elif node.getchild(0).getdata().count("'") == 2:
                        return node.getchild(0).getdata()[1:-1:]
                    else:
                        return self.v_table[node.getchild(0).getdata()]  # 否则查找v_table，返回v_table中的变量值
                elif node.getdata() == '[VARIABLE]':
                    return self.v_table[node.getchild(0).getdata()][recursively_calculate_rvalue(node.getchild(1))]
                elif node.getdata() == '[VISIT]':
                    return self.v_table[node.getchild(0).getdata()].v_table[node.getchild(1).getdata()]
                else:  # 递归地求解表达式
                    if node.getchild(1).getdata() == '-':
                        return recursively_calculate_rvalue(node.getchild(0)) - recursively_calculate_rvalue(
                            node.getchild(2))
                    elif node.getchild(1).getdata() == '+':
                        return recursively_calculate_rvalue(node.getchild(0)) + recursively_calculate_rvalue(
                            node.getchild(2))
                    elif node.getchild(1).getdata() == '*':
                        return recursively_calculate_rvalue(node.getchild(0)) * recursively_calculate_rvalue(
                            node.getchild(2))
                    elif node.getchild(1).getdata() == '/':
                        return recursively_calculate_rvalue(node.getchild(0)) / recursively_calculate_rvalue(
                            node.getchild(2))
                    elif node.getchild(1).getdata() == '//':
                        return recursively_calculate_rvalue(node.getchild(0)) // recursively_calculate_rvalue(
                            node.getchild(2))

            if len(node.getchild(0).getchildren()) == 1:
                lvalue = node.getchild(0).getchild(0).getdata()
                if node.getchild(2).getdata() in ['[VARIABLE]', '[EXPR]', '[TERM]']:
                    rvalue = recursively_calculate_rvalue(node.getchild(2))
                    self.update_v_table(lvalue, rvalue)
                elif node.getchild(2).getdata() == '[AGGREGATION]':
                    rvalue = self.parse_aggregation_to_list(node.getchild(2))
                    self.update_v_table(lvalue, rvalue)
                elif node.getchild(2).getdata() == 'len':
                    rvalue = len(self.v_table[node.getchild(3).getdata()])
                    self.update_v_table(lvalue, rvalue)
                elif node.getchild(2).getdata() == '[CLASS]':
                    n = Node('[INVOKE]')
                    n.add(Node('__init__'))
                    n.add(node.getchild(4))
                    self.v_table[node.getchild(0).getchild(0).getdata()] = Class(dict({}))
                    self.trans(n)
                elif node.getchild(2).getdata() == '[VISIT]':
                    rvalue = self.v_table[node.getchild(2).getchild(0).getdata()].v_table[
                        node.getchild(2).getchild(1).getdata()]
                    self.update_v_table(lvalue, rvalue)
                else:
                    rvalue = self.v_table[node.getchild(2).getdata()][self.v_table[node.getchild(3).getdata()]]
                    self.update_v_table(lvalue, rvalue)
            else:
                if node.getchild(0).getdata() == '[VISIT]':
                    lvalue = node.getchild(0).getchild(1).getdata()
                else:
                    lvalue = node.getchild(0).getchild(0).getdata()

                if node.getchild(2).getdata() in ['[VARIABLE]', '[EXPR]', '[TERM]', '[VISIT]']:
                    rvalue = recursively_calculate_rvalue(node.getchild(2))
                    if node.getchild(0).getdata() == '[VISIT]':
                        self.v_table['self'].v_table[node.getchild(0).getchild(1).getdata()] = rvalue
                    else:
                        index = self.v_table[node.getchild(0).getchild(1).getchild(0).getdata()]
                        self.v_table[lvalue][index] = rvalue
                elif node.getchild(2).getdata() == '[AGGREGATION]':
                    index = self.v_table[node.getchild(0).getchild(1).getchild(0).getdata()]
                    rvalue = self.parse_aggregation_to_list(node.getchild(2))
                    self.v_table[lvalue][index] = rvalue
                elif node.getchild(2).getdata() == 'len':
                    index = self.v_table[node.getchild(0).getchild(1).getchild(0).getdata()]
                    rvalue = len(self.v_table[node.getchild(3).getdata()])
                    self.v_table[lvalue][index] = rvalue
                else:
                    index = self.v_table[node.getchild(0).getchild(1).getchild(0).getdata()]
                    rvalue = self.v_table[node.getchild(2).getdata()][self.v_table[node.getchild(3).getdata()]]
                    self.v_table[lvalue][index] = rvalue

            # print(v_table)
        elif node.getdata() == '[CLASS]':
            t = Translate()
            class_table[node.getchild(0)] = t
            t.trans(node.getchild(1))

        # Print
        elif node.getdata() == '[PRINT]':
            '''print : PRINT '(' variables ')' '''

            def recursively_print(node):
                if len(node.getchildren()) == 1:  # 如果只有一个孩子，触碰到递归边界，打印出该孩子在v_table中的值
                    print(self.v_table[node.getchild(0).getdata()])
                else:  # 不然
                    print(self.v_table[node.getchild(0).getdata()])  # child0 代表了一个变量，打印之
                    recursively_print(node.getchild(1))  # 递归打印 child1，它是一个和当前node具有同样子结构的语法树

            recursively_print(node.getchild(2))

        elif node.getdata() == '[IF]':
            children = node.getchildren()
            if self.trans(children[0]):
                self.trans(children[1])
            else:
                self.trans(children[2])

        elif node.getdata() == '[ELSEIF]':
            children = node.getchildren()
            if len(children) == 1:
                self.trans(children[0])
            else:
                if self.trans(children[0]):
                    self.trans(children[1])
                else:
                    self.trans(children[2])

        elif node.getdata() == '[ELSE]':
            for c in node.getchildren():
                self.trans(c)

        elif node.getdata() == '[FUNCTION]':
            f_table[node.getchild(0).getdata()] = [node.getchild(2), self.parse_aggregation_to_list(node.getchild(1))]
            return

        elif node.getdata() == '[CONDITIONS]':
            return self.trans(node.getchild(0)) and self.trans(node.getchild(2))

        elif node.getdata() == '[CONDITION]':

            # print(v_table)
            left = 0
            if len(node.getchild(0).getchildren()) > 1:
                if node.getchild(0).getchild(1).getdata() == '[VARIABLE]':
                    if node.getchild(0).getchild(1).getchild(0).getdata().isdigit():
                        left = self.v_table[node.getchild(0).getchild(0).getdata()][
                            int(node.getchild(0).getchild(1).getchild(0).getdata())]
                    else:
                        left = self.v_table[node.getchild(0).getchild(0).getdata()][
                            self.v_table[node.getchild(0).getchild(1).getchild(0).getdata()]]
            else:
                left = self.v_table[node.getchild(0).getchild(0).getdata()]
            right = self.v_table[node.getchild(2).getchild(0).getdata()]
            if node.getchild(1).getdata() == '<':
                node.value = left < right
            elif node.getchild(1).getdata() == '>':
                node.value = left > right
            elif node.getchild(1).getdata() == '<=':
                node.value = left <= right
            elif node.getchild(1).getdata() == '>=':
                node.value = left >= right
            elif node.getchild(1).getdata() == '==':
                node.value = left == right
            elif node.getchild(1).getdata() == '!=':
                node.value = left != right

        elif node.getdata() == '[WHILE]':
            self.loop_break_registration.append(True)
            children = node.getchildren()
            while self.loop_break_registration[-1] and self.trans(children[0]):
                for c in children[1:]:
                    self.trans(c)
            else:
                self.loop_break_registration.pop(-1)

        elif node.getdata() == '[FOR]':
            self.loop_break_registration.append(True)
            children = node.getchildren()
            self.trans(children[0])
            while self.loop_break_registration[-1] and self.trans(children[1]):
                self.trans(children[3])
                self.trans(children[2])
            else:
                self.loop_break_registration.pop(-1)

        elif node.getdata() == '[BREAK]':
            self.loop_break_registration[-1] = False

        elif node.getdata() == '[RETURN]':
            self.loop_break_registration.append(False)

        elif node.getdata() == '[INVOKE]':
            args = [self.v_table[x] for x in self.parse_aggregation_to_list(node.getchild(1))]
            f_name = node.getchild(0).getdata()
            context = f_table[f_name]
            t = Translate()
            index = 0
            for i in context[1]:
                t.v_table[i] = args[index]
                index += 1
            t.trans(context[0])

        else:
            for c in node.getchildren():
                self.trans(c)

        return node.value
