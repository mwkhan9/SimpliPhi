key = ["<>",">>","~","&","|"]   

from sympy.abc import *
from sympy.logic import simplify_logic
import re

class dnf():
    def __init__(self,question):
        self.question = self.fixUp(question)
        self.numberOfLogicOperations = self.checkHowManyLogicOperations(self.question)
        
        self.answer,self.listOfSteps,self.listOfResults = self.solve(self.question,self.numberOfLogicOperations,["Start:"],[self.question])

    def fixUp(self,question):
        question = question.replace("∧","&")
        question = question.replace("∨","|")
        question = question.replace("¬","~")
        question = question.replace("↔","<>")
        question = question.replace("→",">>")

        question = question.replace(" ","") #Remove redundant spaces - if any

        return question
    
    def checkHowManyLogicOperations(self,expression):
        numberOfOperations = {"&":0,"~":0,">>":0,"<>":0,"|":0}
        for i in key:
            occurences = expression.count(i)    #Count how many times each logic operation is in the expression
            numberOfOperations[i] = occurences

        return numberOfOperations

    #Remove Bi-Implications (<>):
    def removeBiImp(self,statement):
        (ogleft,ogright) = statement.split('<>',1)  #Split from first occurence of <>
        if (("(") in ogleft) and (ogleft.count("(")!=ogleft.count(")")) :
            openPosition = ogleft.rfind("(")
            left = ogleft[openPosition+1:]
            closedPosition = ogright.find(")")
            right = ogright[:closedPosition]

            statement =  statement.replace((left+"<>"+right),("("+left+">>"+right+")"))

            return statement
        else:
            (left,right) = statement.split('<>',1)  #Split from first occurence of >>
            statement = "("+left+">>"+right+") & ("+right+">>"+left+")"
            return statement

    def reverseReplace(self,string, oldChar, newChar, number):
      update = string.rsplit(oldChar, number)
      changed = newChar.join(update)
      return changed

    #Remove Implications (>>):
    def removeImp(self,statement):
        (ogleft,ogright) = statement.split('>>',1)  #Split from first occurence of >>
        if (("(") in ogleft) and (ogleft.count("(")!=ogleft.count(")")) :

            if ogleft.count(")") == 0:
                openPosition = ogleft.rfind("(")
                left = ogleft[openPosition+1:]
                closedPosition = ogright.find(")")
                right = ogright[:closedPosition]

                statement =  statement.replace((left+">>"+right),("~"+left+"|"+right))

                return statement

            numberNeeded = ogleft.count("(") - ogleft.count(")")
            copy = ogleft
            for i in range(0,numberNeeded):
                copy = self.reverseReplace(copy,'(', 'x', 1)
            openPosition = copy.rfind("(")

            left = ogleft[openPosition+1:]
            closedPosition = ogright.find(")")
            right = ogright[:closedPosition]

            statement =  statement.replace((left+">>"+right),("~"+left+"|"+right))

            return statement
        else:
            (left,right) = statement.split('>>',1)  #Split from first occurence of >>
            statement = "~"+left+"|"+right
            return statement

    #Move Negation (~):
    def moveNeg(self,statement,listOfSteps,listOfResults):
        list = re.findall('\(([^)]+)', statement)  #List of all sub-brackets
        for i in range(len(list)):
            if "~~" in statement:
                statement = statement.replace("~~","")
                listOfSteps.append("Double Negations cancel:")
                listOfResults.append(statement)

            if "~("+list[i]+")" in statement:
                statement = statement.replace("~("+list[i]+")",  "("+str(simplify_logic(eval("~("+list[i]+")")))+")"    ) #I.e. ~(z&x) === ~z|~x
                listOfSteps.append("Open brackets:")
                listOfResults.append(statement)

        #If it's just -A then leave it!
        return statement,listOfSteps,listOfResults

    def solve(self,expression,numberOfLogicOperations,listOfSteps,listOfResults):  
        #List all sub-brackets
        old = expression
        list = re.findall('\(([^)]+)', expression)  #List of all sub-brackets
        #print(list)
        
        for i in range(len(list)):
            if ("<>" in list[i]): #Check if <> is in statement
                expression = expression.replace(list[i],self.removeBiImp(list[i]))  #Replaces all <> within sub-prackets appropriately
                listOfSteps.append("Remove Bi-Implications:")
                listOfResults.append(expression)
                numberOfLogicOperations = self.checkHowManyLogicOperations(expression) #RE-CALCULATE as new symbols may have formed

            if (">>" in list[i]): #Check if >> is in statement
                expression = expression.replace(list[i],self.removeImp(list[i]))  #Replaces all <> within sub-prackets appropriately
                listOfSteps.append("Remove Implications:")
                listOfResults.append(expression)
                numberOfLogicOperations = self.checkHowManyLogicOperations(expression)

        #Replaces all <> outside of sub-prackets 
        numberOfBiImp = numberOfLogicOperations["<>"]
        while numberOfBiImp>0:
            expression = self.removeBiImp(expression)
            listOfSteps.append("Remove Bi-Implications:")
            listOfResults.append(expression)
            numberOfLogicOperations = self.checkHowManyLogicOperations(expression)
            numberOfBiImp = numberOfLogicOperations["<>"]

        #Replaces all >> outside of sub-prackets 
        numberOfImp = numberOfLogicOperations[">>"]
        while numberOfImp>0:
            expression = self.removeImp(expression)
            listOfSteps.append("Remove Implications:")
            listOfResults.append(expression)
            numberOfLogicOperations = self.checkHowManyLogicOperations(expression)
            numberOfImp = numberOfLogicOperations[">>"]

        #Check no more symbols are in the expression
        while (numberOfLogicOperations[">>"]>0) or (numberOfLogicOperations["<>"]>0):
            expression = solve(expression,numberOfLogicOperations,listOfSteps,listOfResults)
            
        expression,listOfSteps,listOfResults = self.moveNeg(expression,listOfSteps,listOfResults)    #Move negations

        listOfSteps.append("Tidy Up / Move disjunctions outwards:") #i.e.( remove redundant parenthesis if needed) & (Move disjunctions outwards if needed)
        expression = simplify_logic(eval(expression),'dnf')
        listOfResults.append(expression)
            
        return expression,listOfSteps,listOfResults

    def output(self):
        return self.answer,self.listOfSteps,self.listOfResults 

if __name__ == "__main__":

    expression = "~( A >> B)"
    #expression = "(~P|~Q)>>(P <> ~Q)"
    #expression = "(P>>Q)<>(Q>>P)"
    #expression = "P<>(~Q|R)"
    #expression = "((P∨Q)>>R)∨P"
    expression = "(A&C)&(P<>(Q|Z))"

    #print("Simplified:",simplify_logic(expression,'dnf')) #- QUICKLY FIND THE END SOLUTION IF NEEDED

    test = dnf(expression)
    value,listOfSteps,listOfResults = test.output()

    #Below is for all steps!
    for i in range(len(listOfResults)):
        print(listOfSteps[i])
        print(listOfResults[i])


