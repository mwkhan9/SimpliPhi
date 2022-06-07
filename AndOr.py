'''
First step is to remove the bi-Implications as there are no equivalences for
Bi-Implications being simplified into the Conjunction/Disjunction. This can be done
splitting the statement each side of the symbol, simplifying each side of the "AND"
symbol

To simplify each side of the statement we need a library of some sort with all the
propositional formulas which can simplify each sub-statement into and/not form.

I am assuming that we will also need some data structure which outlines which symbols
have higher presidence over other symbols. (ASSUMPTION)

Each sub-statement is in minimum form when we can no longer use any of the propositional
formulas in our ""library"" of formulas on the sub-statements either side of the AND.
'''

from sympy.abc import *
from sympy.logic import simplify_logic
import re
working = []
argument = []

def reset():
    global working
    working = []

class AON:
    def __init__(self, question):
        self.question = question
        working.append(question)
        self.getArguments(question)
        
        self.simplifyFormulas(question)

    def getArguments(self,expression):
        argument = []
        alpha = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
                 "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        expression = expression.lower()
        numberofUses = {"a": 0, "b": 0, "c": 0, "d": 0, "e": 0, "f": 0, "g": 0, "h": 0, "i": 0, "j": 0,
                        "k": 0, "l": 0, "m": 0, "n": 0, "o": 0, "p": 0, "q": 0, "r": 0, "s": 0,
                        "t": 0, "u": 0, "v": 0, "w": 0, "x": 0, "y": 0, "z": 0
                        }
        for i in alpha:
            occurences = expression.count(i)
            numberofUses[i] = occurences

        for i in numberofUses:
            if numberofUses[i] != 0:
                argument.append(i)

        return argument

    def output(self):
        return working

    def split(self, word):
        return [char for char in word]

    def simplifyFormulas(self, expression):
        expression = expression.replace(' ', '')
    
        # (¬¬p) = p
        if '(¬¬' in expression and len(expression) >= 4:
            (left, right) = expression.split("(¬¬", 1)
            lst = self.split(right)
            lst2 = self.split(left)
            if lst[1] == ')':
                del lst[1]
                lst3 = lst2 + lst
                expression = ''.join(lst3)
                working.append(expression)
    
        # ¬¬p = p
        if "¬¬" in expression:
            expression = expression.replace("¬¬", "")
            working.append(expression)
    
        # ¬(¬p) = p
        if "¬(¬" in expression:
            (left, right) = expression.split("¬(¬", 1)
            lst = self.split(right)
            lst2 = self.split(left)
            if lst[1] == ')':
                del lst[1]
                lst3 = lst2 + lst
                expression = ''.join(lst3)
                working.append(expression)
    
        # (p ∧ q) ≡ ¬ (¬ p ∨ ¬ q)
        '''if "¬(¬" in expression and len(expression) >= 8:
            (left,right) = expression.self.split("¬(¬", 1)
            lst = self.split(right)
            lst2 = self.split(left)
            if lst[1] == '∨' and lst[2] == '¬' and lst[4] == ')' and lst[0] != lst[3]:
                del lst[2]
                lst[1] = '∧'
                lst2.append('(')
                lst3 = lst2 + lst
                expression = ''.join(lst3)
                working.append(expression)'''
    
        # (p ∧ q ∧ r) ≡ ¬ (¬ p ∨ ¬ q ∨ ¬ r) or any number of propositions
        if "¬(¬" in expression and len(expression) >= 8:
            arguments = self.getArguments(expression)
            (left, right) = expression.split("¬(¬", 1)
            lst = self.split(right)
            lst2 = self.split(left)
            count = 0
            # how many arguments are in this part
            for i in arguments:
                if i in lst:
                    count = count + 1
            # checking for unions and negations
            counter = 0
            counts = 0
            index = 0
            indicies = 0
            brack = 0
            for i in range(0, len(arguments)):
                index = (3 * i) - 2
                if len(lst)>index:
                    if lst[index] == '∨':
                        counter = counter + 1
                        if counter == count - 1:
                            for i in range(0, len(arguments)):
                                indicies = (3 * i) - 1
                                if lst[indicies] == '¬':
                                    counts = counts + 1
                                    if counts == count - 1:
                                        brack = 3 * len(arguments) - 2
                                        if lst[brack] == ')':
                                            right = right.replace('¬', '')
                                            right = right.replace('∨', '∧')
                                            lst2.append('(')
                                            lst = self.split(right)
                                            lst3 = lst2 + lst
                                            expression = ''.join(lst3)
                                            working.append(expression)
    
        # p ∨ q ≡ ¬ (¬ p ∧ ¬ q)
        '''if "¬(¬" in expression and len(expression) >= 8:
            (left,right) = expression.self.split("¬(¬", 1)
            lst = self.split(right)
            lst2 = self.split(left)
            if lst[1] == '∧' and lst[2] == '¬' and lst[4] == ')' and lst[0] != lst[3]:
                del lst[2]
                lst[1] = '∨'
                lst2.append('(')
                lst3 = lst2 + lst
                expression = ''.join(lst3)
                working.append(expression)'''
    
        # p ∨ q ≡ ¬ (¬ p ∧ ¬ q ∧ ¬ r ∧ ¬ a ∧ ¬ b) or any number of propositions
        if "¬(¬" in expression and len(expression) >= 8:
            arguments = self.getArguments(expression)
            (left, right) = expression.split("¬(¬", 1)
            lst = self.split(right)
            lst2 = self.split(left)
            count = 0
            # how many arguments are in this part
            for i in arguments:
                if i in lst:
                    count = count + 1
            # checking for unions and negations
            counter = 0
            counts = 0
            index = 0
            indicies = 0
            brack = 0
            for i in range(0, len(arguments)):
                index = (3 * i) - 2
                if len(lst)>index:
                    if lst[index] == '∧':
                        counter = counter + 1
                        if counter == count - 1:
                            for i in range(0, len(arguments)):
                                indicies = (3 * i) - 1
                                if lst[indicies] == '¬':
                                    counts = counts + 1
                                    if counts == count - 1:
                                        brack = 3 * len(arguments) - 2
                                        if lst[brack] == ')':
                                            right = right.replace('¬', '')
                                            right = right.replace('∧', '∨')
                                            lst2.append('(')
                                            lst = self.split(right)
                                            lst3 = lst2 + lst
                                            expression = ''.join(lst3)
                                            working.append(expression)
    
        # p ∧ q ≡ ¬(p → ¬q)
        if "¬(" in expression and len(expression) >= 7:
            (left, right) = expression.split("¬(", 1)
            lst = self.split(right)
            if lst[1] == '→' and lst[2] == '¬':
                if lst[4] == ")":
                    lst[1] = '∧'
                    del lst[2]
                    lst2 = self.split(left)
                    lst2.append("(")
                    lst3 = lst2 + lst
                    expression = ''.join(lst3)
                    working.append(expression)
    
        # ¬(p → ¬(q ∨ r ∨ s)) or any infinite amount of propositional letters
        if "¬(" in expression and len(expression) >= 7:
            arguments = self.getArguments(expression)
            (left, right) = expression.split("¬(", 1)
            lst = self.split(right)
            lst2 = self.split(left)
            count = 0
            # how many arguments are in this part
            for i in arguments:
                if i in lst:
                    count = count + 1
            # checking for unions and negations
            counter = 0
            counts = 0
            index = 0
            indicies = 0
            brack = 0
            if lst[1] == '→' and lst[2] == '¬' and lst[3] == '(' and count > 2:
                count = count - 2
                end = 3 + ((len(arguments) * 2) - 1)
                if len(lst) > end:
                    if lst[end] == ')':
                        for i in range(3, len(lst) - 1):
                            # count = count - 2
                            if lst[i] == '∨':
                                counter = counter + 1
                                if count == counter:
                                    if '∨∨' not in lst:
                                        if lst[5] == '∨':
                                            right = right.replace('¬', '')
                                            right = right.replace('→', '∧')
                                            lst2.append('(')
                                            lst = self.split(right)
                                            lst3 = lst2 + lst
                                            expression = ''.join(lst3)
                                            working.append(expression)
    
        # ¬(p → ¬(q ∧ r ∧ s ∧ w))
        if "¬(" in expression and len(expression) >= 7:
            arguments = self.getArguments(expression)
            (left, right) = expression.split("¬(", 1)
            lst = self.split(right)
            lst2 = self.split(left)
            count = 0
            # how many arguments are in this part
            for i in arguments:
                if i in lst:
                    count = count + 1
            # checking for unions and negations
            counter = 0
            counts = 0
            index = 0
            indicies = 0
            brack = 0
            if lst[1] == '→' and lst[2] == '¬' and lst[3] == '(' and count > 2:
                count = count - 2
                end = 3 + ((len(arguments) * 2) - 1)
                if len(lst)>end:
                    if lst[end] == ')':
                        for i in range(3, len(lst) - 1):
                            # count = count - 2
                            if lst[i] == '∧':
                                counter = counter + 1
                                if count == counter:
                                    if '∧∧' not in lst:
                                        if lst[5] == '∧':
                                            right = right.replace('¬', '')
                                            right = right.replace('→', '∧')
                                            lst2.append('(')
                                            lst = self.split(right)
                                            if lst[end - 1] == ')':
                                                del lst[end - 1]
                                            if lst[2] == '(':
                                                del lst[2]
                                            lst3 = lst2 + lst
                                            expression = ''.join(lst3)
                                            working.append(expression)
                                            break
    
        # (p ∨ q) ≡ (¬p → q)
        if "(¬" in expression and len(expression) >= 6:
            (left, right) = expression.split("(¬", 1)
            lst = self.split(right)
            if lst[1] == '→' and lst[3] == ')':
                lst[1] = '∨'
                lst2 = self.split(left)
                lst2.append("(")
                lst3 = lst2 + lst
                expression = ''.join(lst3)
                working.append(expression)
    
        # (p ∨ q) ≡ (¬p → (q ∧ r ∧ s)) or any amount of propositional letters
        if "(¬" in expression and len(expression) >= 6:
            arguments = self.getArguments(expression)
            (left, right) = expression.split("(¬", 1)
            lst = self.split(right)
            lst2 = self.split(left)
            count = 0
            # how many arguments are in this part
            for i in arguments:
                if i in lst:
                    count = count + 1
            # checking for unions and negations
            counter = 0
            counts = 0
            index = 0
            indicies = 0
            brack = 0
            if lst[1] == '→' and lst[2] == '(' and count > 2:
                count = count - 2
                end = 2 + ((len(arguments) * 2) - 1)
                if lst[end] == ')':
                    for i in range(2, len(lst) - 1):
                        # count = count - 2
                        if lst[i] == '∧':
                            counter = counter + 1
                            if count == counter:
                                if '∧∧' not in lst:
                                    if lst[4] == '∧':
                                        lst[1] = '∨'
                                        lst2.append('(')
                                        # lst = self.split(right)
                                        lst3 = lst2 + lst
                                        expression = ''.join(lst3)
                                        working.append(expression)
                                        break
    
        # (p ∨ q) ≡ (¬p → (q ∨ r)) or any amount of propositional letters
        if "(¬" in expression and len(expression) >= 6:
            arguments = self.getArguments(expression)
            (left, right) = expression.split("(¬", 1)
            lst = self.split(right)
            lst2 = self.split(left)
            count = 0
            # how many arguments are in this part
            for i in arguments:
                if i in lst:
                    count = count + 1
            # checking for unions and negations
            counter = 0
            counts = 0
            index = 0
            indicies = 0
            brack = 0
            if lst[1] == '→' and lst[2] == '(' and count > 2:
                count = count - 2
                end = 2 + ((len(arguments) * 2) - 1)
                if lst[end] == ')':
                    for i in range(2, len(lst) - 1):
                        # count = count - 2
                        if lst[i] == '∨':
                            counter = counter + 1
                            if count == counter:
                                if '∨∨' not in lst:
                                    if lst[4] == '∨':
                                        lst[1] = '∨'
                                        lst2.append('(')
                                        # lst = self.split(right)
                                        if lst[end - 1] == ')':
                                            del lst[end - 1]
                                        if lst[2] == '(':
                                            del lst[2]
                                        lst3 = lst2 + lst
                                        expression = ''.join(lst3)
                                        working.append(expression)
                                        break
    
        # p ∨ q ≡ ¬p → q
        if "¬" in expression and len(expression) <= 4:
            (left, right) = expression.split("¬", 1)
            lst = self.split(right)
            if lst[1] == '→' and lst[0] != lst[2] and len(lst) == 3:
                lst[1] = '∨'
                lst2 = self.split(left)
                lst3 = lst2 + lst
                expression = ''.join(lst3)
                working.append(expression)
    
        # (p ∨ q) ≡ ¬p → (q ∧ r ∧ s)
        if "¬" in expression and len(expression) >= 6:
            arguments = self.getArguments(expression)
            (left, right) = expression.split("¬", 1)
            lst = self.split(right)
            lst2 = self.split(left)
            count = 0
            # how many arguments are in this part
            for i in arguments:
                if i in lst:
                    count = count + 1
            # checking for unions and negations
            counter = 0
            counts = 0
            index = 0
            indicies = 0
            brack = 0
            if lst[1] == '→' and lst[2] == '(' and count > 2:
                count = count - 2
                end = 2 + ((len(arguments) * 2) - 1)
                if lst[end - 1] == ')':
                    for i in range(2, len(lst) - 1):
                        # count = count - 2
                        if lst[i] == '∧':
                            counter = counter + 1
                            if count == counter:
                                if '∧∧' not in lst:
                                    if lst[4] == '∧':
                                        lst[1] = '∨'
                                        lst2.append('(')
                                        # lst = self.split(right)
                                        lst3 = lst2 + lst
                                        expression = ''.join(lst3)
                                        working.append(expression)
                                        break
    
        # (p ∨ q) ≡ ¬p → (q ∨ r ∨ s) or any amount of propositional letters
        if "¬" in expression and len(expression) >= 6:
            arguments = self.getArguments(expression)
            (left, right) = expression.split("¬", 1)
            lst = self.split(right)
            lst2 = self.split(left)
            count = 0
            # how many arguments are in this part
            for i in arguments:
                if i in lst:
                    count = count + 1
            # checking for unions and negations
            counter = 0
            counts = 0
            index = 0
            indicies = 0
            brack = 0
            if lst[1] == '→' and lst[2] == '(' and count > 2:
                count = count - 2
                end = 2 + ((len(arguments) * 2) - 1)
                if lst[end - 1] == ')':
                    for i in range(2, len(lst) - 1):
                        # count = count - 2
                        if lst[i] == '∨':
                            counter = counter + 1
                            if count == counter:
                                if '∨∨' not in lst:
                                    if lst[4] == '∨':
                                        lst[1] = '∨'
                                        lst2.append('(')
                                        # lst = self.split(right)
                                        if lst[2] == '(':
                                            del lst[2]
                                        lst3 = lst2 + lst
                                        expression = ''.join(lst3)
                                        working.append(expression)
                                        break
    
        # ¬(p ∨ q) = Nothing
        if '¬(' in expression and len(expression) >= 6:
            (left, right) = expression.split("¬(", 1)
            lst = self.split(right)
            lst2 = self.split(left)
            if lst[1] == '∨' and lst[3] == ')' and lst[0] != lst[2]:
                del lst[0]
                del lst[0]
                del lst[0]
                del lst[0]
                lst3 = lst2 + lst
                expression = ''.join(lst3)
                working.append(expression)
    
        # ¬(p ∨ q ∨ r ∨ s ∨ t) = Nothing can use any number of propositions
        if '¬(' in expression and len(expression) >= 6:
            arguments = self.getArguments(expression)
            (left, right) = expression.split("¬(", 1)
            lst = self.split(right)
            lst2 = self.split(left)
            count = 0
            # how many arguments are in this part
            for i in arguments:
                if i in lst:
                    count = count + 1
            # checking for unions and negations
            counter = 0
            counts = 0
            index = 0
            indicies = 0
            brack = 0
            if count > 2:
                count = count - 1
                end = (len(arguments) * 2) - 1
                if len(lst)>end:
                    if lst[end] == ')':
                        for i in range(0, len(lst) - 1):
                            # count = count - 2
                            if lst[i] == '∨':
                                counter = counter + 1
                                if count == counter:
                                    if '∨∨' not in lst:
                                        if lst[1] == '∨':
                                            for i in range(0, end + 1):
                                                del lst[0]
                                            lst3 = lst2 + lst
                                            expression = ''.join(lst3)
                                            working.append(expression)
                                            break
    
        # p ∨ (p ∧ q) ≡ p
        if '∨' in expression and len(expression) >= 7:
            (left, right) = expression.split("∨", 1)
            lst = self.split(right)
            lst2 = self.split(left)
            if lst[0] == '(' and lst[2] == '∧' and lst[4] == ')' and lst[1] != lst[3] and lst2[-1] == lst[1] and lst2[-1] != \
                    lst[3]:
                del lst[0]
                del lst[0]
                del lst[0]
                del lst[0]
                del lst[0]
                lst3 = lst2 + lst
                expression = ''.join(lst3)
                working.append(expression)
    
        # p ∨ (q ∧ p) ≡ p
        if '∨' in expression and len(expression) >= 7:
            arguments = self.getArguments(expression)
            (left, right) = expression.split("∨", 1)
            lst = self.split(right)
            lst2 = self.split(left)
            if lst[0] == '(' and lst[2] == '∧' and lst[4] == ')' and lst[1] != lst[3] and lst2[-1] != lst[1] and lst2[-1] == \
                    lst[3]:
                del lst[0]
                del lst[0]
                del lst[0]
                del lst[0]
                del lst[0]
                lst3 = lst2 + lst
                expression = ''.join(lst3)
                working.append(expression)
    
        # p ∨ (q ∧ p ∧ r) ≡ p or any number of propositions
        if '∨' in expression and len(expression) >= 7:
            arguments = self.getArguments(expression)
            (left, right) = expression.split("∨", 1)
            lst = self.split(right)
            lst2 = self.split(left)
            count = 0
            # how many arguments are in this part
            for i in arguments:
                if i in lst:
                    count = count + 1
            # checking for unions and negations
            counter = 0
            counts = 0
            index = 0
            indicies = 0
            brack = 0
            if count > 2:
                count = count - 1
                # end = (len(arguments) * 2)
                # f lst[end] == ')':
                for i in range(0, len(lst) - 1):
                    # count = count - 2
                    if lst[i] == '∧':
                        counter = counter + 1
                        if count == counter:
                            if '∧∧' not in lst:
                                if lst[2] == '∧':
                                    end = (len(arguments) * 2)
                                    if len(lst) > end:
                                        if lst[end] == ')':
                                            for i in range(0, end + 1):
                                                del lst[0]
                                            lst3 = lst2 + lst
                                            expression = ''.join(lst3)
                                            working.append(expression)
                                            break
    
        # p ∧ (p ∨ q) ≡ p
        if '∧' in expression and len(expression) >= 7:
            (left, right) = expression.split("∧", 1)
            lst = self.split(right)
            lst2 = self.split(left)
            if lst[0] == '(' and lst[2] == '∨' and lst[4] == ')' and lst[1] != lst[3] and lst2[-1] == lst[1] and lst2[-1] != \
                    lst[3]:
                del lst[0]
                del lst[0]
                del lst[0]
                del lst[0]
                del lst[0]
                lst3 = lst + lst2
                expression = ''.join(lst3)
                working.append(expression)
    
        # p ∧ (q ∨ p) ≡ p
        if '∧' in expression and len(expression) >= 7:
            (left, right) = expression.split("∧", 1)
            lst = self.split(right)
            lst2 = self.split(left)
            if lst[0] == '(' and lst[2] == '∨' and lst[4] == ')' and lst[1] != lst[3] and lst2[-1] != lst[1] and lst2[-1] == \
                    lst[3]:
                del lst[0]
                del lst[0]
                del lst[0]
                del lst[0]
                del lst[0]
                lst3 = lst + lst2
                expression = ''.join(lst3)
                working.append(expression)
    
        # p ∧ (q ∨ p ∨ r ∨ s) ≡ p or ant number of arguments
        if '∧' in expression and len(expression) >= 7:
            arguments = self.getArguments(expression)
            (left, right) = expression.split("∧", 1)
            lst = self.split(right)
            lst2 = self.split(left)
            count = 0
            # how many arguments are in this part
            for i in arguments:
                if i in lst:
                    count = count + 1
            # checking for unions and negations
            counter = 0
            counts = 0
            index = 0
            indicies = 0
            brack = 0
            if count > 2:
                count = count - 1
                # end = (len(arguments) * 2)
                # if lst[end] == ')':
                for i in range(0, len(lst) - 1):
                    # count = count - 2
                    if lst[i] == '∨':
                        counter = counter + 1
                        if count == counter:
                            if '∨∨' not in lst:
                                if lst[2] == '∨':
                                    end = (len(arguments) * 2)
                                    if len(lst) > end:
                                        if lst[end] == ')':
                                            for i in range(0, end + 1):
                                                del lst[0]
                                            lst3 = lst2 + lst
                                            expression = ''.join(lst3)
                                            working.append(expression)
                                            break
    
        # (p ∨ p) = p
        if '∨' in expression and len(expression) >= 5:
            (left, right) = expression.split("∨", 1)
            lst = self.split(right)
            lst2 = self.split(left)
            if lst[0] == lst2[-1] and lst[1] == ')' and lst2[-2] == '(':
                del lst[1]
                del lst2[-2]
                del lst[0]
                lst3 = lst2 + lst
                expression = ''.join(lst3)
                working.append(expression)
    
        # p ∨ p = p
        if '∨' in expression:  # and len(expression) <= 3:
            (left, right) = expression.split("∨", 1)
            lst = self.split(right)
            lst2 = self.split(left)
            if lst[0] == lst2[-1]:  # and len(lst) == 1 and len(lst2) == 1:
                del lst[0]
                lst3 = lst2 + lst
                expression = ''.join(lst3)
                working.append(expression)
    
        # (p ∧ p) = p
        if '∧' in expression and len(expression) >= 5:
            (left, right) = expression.split("∧", 1)
            lst = self.split(right)
            lst2 = self.split(left)
            if lst[0] == lst2[-1] and lst[1] == ')' and lst2[-2] == '(':
                del lst[1]
                del lst2[-2]
                del lst[0]
                lst3 = lst2 + lst
                expression = ''.join(lst3)
                working.append(expression)
    
        # p ∧ p = p
        if '∧' in expression:  # and len(expression) <= 3:
            (left, right) = expression.split("∧", 1)
            lst = self.split(right)
            lst2 = self.split(left)
            if lst[0] == lst2[-1]:  # and len(lst) == 1 and len(lst2) == 1:
                del lst[0]
                lst3 = lst2 + lst
                expression = ''.join(lst3)
                working.append(expression)
    
        if '(' in expression and len(expression) >= 11:
            (left, right) = expression.split("(", 1)
            lst = self.split(right)
            lst2 = self.split(left)
            if lst[1] == '∨' and lst[3] == ')' and lst[4] == '∧' and lst[5] == '(' and lst[7] == '∨' and lst[9] == ')' \
                    and lst[0] != lst[2] and lst[6] != lst[8]:
    
                # p ∨ (q ∧ r) ≡ (p ∨ q) ∧ (p ∨ r)
                if lst[0] == lst[6] and lst[0] != lst[8] and lst[2] != lst[6] and lst[2] != lst[8]:
                    prop = lst[2]
                    (l1, r1) = expression.split(lst[2], 1)
                    r = self.split(r1)
                    l = self.split(l1)
                    del l[-3]
                    r[0] = prop
                    l.append('(')
                    r[4] = '∧'
                    del r[1]
                    del r[1]
                    del r[1]
                    lst3 = lst2 + l + r
                    expression = ''.join(lst3)
                    working.append(expression)
    
                # p ∨ (q ∧ r) ≡ (p ∨ q) ∧ (r ∨ p)
                if lst[0] == lst[8] and lst[0] != lst[6] and lst[2] != lst[6] and lst[2] != lst[8]:
                    prop = lst[2]
                    (l1, r1) = expression.split(lst[2], 1)
                    r = self.split(r1)
                    l = self.split(l1)
                    del l[-3]
                    r[0] = prop
                    l.append('(')
                    del r[2]
                    del r[3]
                    del r[3]
                    lst3 = lst2 + l + r
                    expression = ''.join(lst3)
                    working.append(expression)
    
                # q ∨ (p ∧ r) ≡ (p ∨ q) ∧ (q ∨ r)
                if lst[0] != lst[8] and lst[0] != lst[6] and lst[2] == lst[6] and lst[2] != lst[8]:
                    prop = lst[2]
                    (l1, r1) = expression.split(lst[2], 1)
                    r = self.split(r1)
                    l = self.split(l1)
                    r[0] = prop
                    r[1] = '∨'
                    r[3] = l[-2]
                    r[4] = '∧'
                    lst3 = lst2 + l + r
                    expression = ''.join(r)
                    working.append(expression)
    
                # q ∨ (p ∧ r) ≡ (p ∨ q) ∧ (r ∨ q)
                if lst[0] != lst[8] and lst[0] != lst[6] and lst[2] != lst[6] and lst[2] == lst[8]:
                    prop = lst[2]
                    (l1, r1) = expression.split(lst[2], 1)
                    r = self.split(r1)
                    l = self.split(l1)
                    r[0] = prop
                    r[1] = '∨'
                    r[4] = '∧'
                    r[5] = l[-2]
                    lst3 = lst2 + l + r
                    expression = ''.join(r)
                    working.append(expression)
    
            if lst[1] == '∧' and lst[3] == ')' and lst[4] == '∨' and lst[5] == '(' and lst[7] == '∧' and lst[9] == ')' \
                    and lst[0] != lst[2] and lst[6] != lst[8]:
    
                # p ∧ (q ∨ r) ≡ (p ∧ q) ∨ (p ∧ r)
                if lst[0] == lst[6] and lst[0] != lst[8] and lst[2] != lst[6] and lst[2] != lst[8]:
                    prop = lst[2]
                    (l1, r1) = expression.split(lst[2], 1)
                    r = self.split(r1)
                    l = self.split(l1)
                    del l[-3]
                    r[0] = prop
                    l.append('(')
                    r[4] = '∨'
                    del r[1]
                    del r[1]
                    del r[1]
                    lst3 = lst2 + l + r
                    expression = ''.join(lst3)
                    working.append(expression)
    
                # p ∧ (q ∨ r) ≡ (p ∧ q) ∨ (r ∧ p)
                if lst[0] == lst[8] and lst[0] != lst[6] and lst[2] != lst[6] and lst[2] != lst[8]:
                    prop = lst[2]
                    (l1, r1) = expression.split(lst[2], 1)
                    r = self.split(r1)
                    l = self.split(l1)
                    del l[-3]
                    r[0] = prop
                    l.append('(')
                    r[4] = '∧'
                    del r[2]
                    del r[3]
                    del r[3]
                    lst3 = lst2 + l + r
                    expression = ''.join(lst3)
                    working.append(expression)
    
                # q ∧ (p ∨ r) ≡ (p ∧ q) ∨ (q ∧ r)
                if lst[0] != lst[8] and lst[0] != lst[6] and lst[2] == lst[6] and lst[2] != lst[8]:
                    prop = lst[2]
                    (l1, r1) = expression.split(lst[2], 1)
                    r = self.split(r1)
                    l = self.split(l1)
                    r[0] = prop
                    r[1] = '∧'
                    r[3] = l[-2]
                    r[4] = '∨'
                    lst3 = lst2 + r
                    expression = ''.join(lst3)
                    working.append(expression)
    
                # q ∧ (r ∨ p) ≡ (p ∧ q) ∨ (r ∧ q)
                if lst[0] != lst[8] and lst[0] != lst[6] and lst[2] != lst[6] and lst[2] == lst[8]:
                    prop = lst[2]
                    (l1, r1) = expression.split(lst[2], 1)
                    r = self.split(r1)
                    l = self.split(l1)
                    r[0] = prop
                    r[1] = '∧'
                    r[4] = '∨'
                    r[5] = l[-2]
                    lst3 = lst2 + r
                    expression = ''.join(lst3)
                    working.append(expression)
    
        return expression
    
    
    # so self.split the expression here and then you do index like below. That may not work so maybe you can change expression into
    # a list of characters and then check if the characters match the symbols. Do it by spacing, forget the propositions for now
    # can forget propositions as you can just replace the characters in the array however much you want then convert back into a string
    
    '''
    p ∨ (q ∧ r) ≡ (p ∨ q) ∧ (p ∨ r) DONE -- -----
    p ∧ (q ∨ r) ≡ (p ∧ q) ∨ (p ∧ r) DONE -- ------
    p ∨ (p ∧ q) ≡ p DONE - ----
    p ∧ (p ∨ q) ≡ p DONE -------
    p ∧ p = p DONE - -------
    p ∨ p = p DONE - -------
    p ∨ q ≡ ¬p → q DONE - ------ 
    p ∧ q ≡ ¬(p → ¬q) DONE - ----
    ¬(¬p) = p DONE - -------
    ¬(p ∨ q) = Nothing DONE - -----
    p ∧ q ≡ ¬ (¬ p ∨ ¬ q) ---
    p ∨ q ≡ ¬ (¬ p ∧ ¬ q) ---
    '''
    
    
    # Remove Bi-Implications (<>):
    def removeBiImp(expression):
        if '↔' in expression:
            (left, right) = expression.self.split('↔', 1)  # self.split from first occurence of <>
            expression = "(" + left + " → " + right + ") ∧ (" + right + " → " + left + ")"
            return expression
    
    
    def removeImp(expression):
        (left, right) = expression.self.split('→', 1)  # self.split from first occurence of >>
        expression = "¬" + left + "∨" + right
        return expression
    
if __name__ == "__main__":
    question = '(p ∨ q) ∧ (¬¬p ∨ r)'
    question = '(p ∨ q) ∧ (¬¬p ∨ r)  ∨ (q→r)'
    getArguments(question)
    removeBiImp(question)
    finished = False
    while finished == False:
        len1 = len(logic)
        logic = simplifyFormulas(question)
        len2 = len(logic)
        if len1 - len2 == 0:
            finished = True
    for step in working:
        print(step)

    # simplifyFormulas('(p ∨ q) ∧ (¬¬p ∨ r)')
    
    
    # need to get amount of arguments in this string and then use that to iterate over some formulas so the formulas
    # can account for any number of arguments
    
    '''¬ (¬ p ∧ ¬ q)
    (p ∨ q) ∧ (p ∨ r)
    ¬(p → ¬(q ∧ r ∧ s))
    p ∨ (p ∧ q)
    p ∨ (p ∧ q ∧ r  ∧  s  ∧ t  ∧ u)
    p ∨ (p ∧ q) ∨ (¬p → q)
    p ∨ (p ∧ q) ∨  (¬¬p)'''
