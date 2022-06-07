from DNF import *
from TruthTable import *
from AndOr import*

class file():
    def __init__(self,filename):
        self.numberOfQuestions = 0
        self.listOfQuestions = {}
        self.importQuestions(filename)

    def importQuestions(self,filename):
        file = open(filename, "r")
        questionList = []
        typeList = []
        for line in file:
            question = line.split(":")[0]
            questionList.append(question)

            typeOfQuestion = line.split(":")[1]
            typeList.append(typeOfQuestion)

            question = question.replace(" ","") #Remove redundant spaces - if any
            typeOfQuestion = typeOfQuestion.replace(" ","") 
            
            self.createObjects(question,typeOfQuestion)
        
        return questionList, typeList
    
    def createObjects(self,q,t):
        t = t.replace('\n','')
        if t == "DNF":
            question = dnf(q)
            #self.listOfQuestions.append(question)
            self.listOfQuestions[question] = "DNF"
            self.numberOfQuestions+=1
        elif t =="TT":
            question = TruthTable(q)
            self.listOfQuestions[question] = "TT"
            self.numberOfQuestions+=1
        elif t =="AON":
            question = AON(q)
            self.listOfQuestions[question] = "AON"
            self.numberOfQuestions+=1

    def solveAll(self):
        for question in self.listOfQuestions:
            if self.listOfQuestions[question] =="DNF":
                #questionObject = dnf(question)
                value,listOfSteps,listOfResults = question.output()

                #Below outputs all the steps!
                for i in range(len(listOfResults)):
                    print(listOfSteps[i])
                    print(listOfResults[i])

                print()

            elif self.listOfQuestions[question] =="TT":
                print(question.question)
                answer = question.gentable()
                print(answer)
                print()

            elif self.listOfQuestions[question] =="AON":
                #print(question.question)
                workings = question.output()
                for line in workings:
                    print(line)

    def solveSeperate(question):
        question = dnf(question)
        value,listOfSteps,listOfResults = question.output()

        return listOfSteps, listOfResults

######## I Added
    def solveAON(question):
        question = AON(question)
        workings = question.output()
        reset()

        return workings

######## 
    
    def showSeperateTT(question):
        question = TruthTable(str(question))
        result = question.gentable()
        print(result)
        return result


test = file("questions.txt")
test.solveAll()


