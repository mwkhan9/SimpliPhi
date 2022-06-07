alpha = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
         "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
import ttg

class TruthTable():
    def __init__(self, question):
        self.question = question
        
        self.arguments = []
        self.statement = []

        self.getArguments()

    def getArguments(self):
        expression = self.question.lower()
        numberofUses = {"a":0, "b":0, "c":0, "d":0, "e":0, "f":0, "g":0, "h":0, "i":0, "j":0,
            "k":0, "l":0, "m":0, "n":0, "o":0, "p":0, "q":0, "r":0, "s":0,
            "t":0, "u":0, "v":0, "w":0, "x":0, "y":0, "z":0
        }
        for i in alpha:
            occurences = expression.count(i)
            numberofUses[i] = occurences

        for i in numberofUses:
            if numberofUses[i] != 0:
                self.arguments.append(i)

    def gentable(self):
        expression = self.question
        expression = expression.replace('∨', ' or ')
        expression = expression.replace('∧', ' and ')
        expression = expression.replace('¬', ' not ')
        
        expression = expression.replace('>>', '=>')
        expression = expression.replace('<>', '=')
        expression = expression.replace('↔', '=')
        expression = expression.replace('→', '=>')

        expression = expression.lower()
        self.statement.append(expression)
        return ttg.Truths(self.arguments,self.statement)

        
if __name__ == "__main__":
    exp = input("Enter expression: ")
    table = TruthTable(exp)
    print(table.gentable())
    
