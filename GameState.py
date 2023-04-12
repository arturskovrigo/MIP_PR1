
class GameState:    #Klase esošā spēles stāvokļa aprakstīšanai
    def __init__(self):
        self.startValue = 100
        self.curValue = 100
        self.isPlayersTurn = True
        self.botText = "Bot hasn't acted yet"
        self.lastBotAction = 0  #iepriekšējais bota gājiens priekš orientēšanās kokā
        self.lastHumanAction = 0 # iepriekšējais cilvēka gājiens priekš orientēšanās kokā
        self.lastAction = 0 # lai atvieglotu koku
        self.children = []
        self.parent = None
        self.nodeValue = None
        
    def print(self):
        print(str(self.curValue))

    def submit(self, num, startingPlayer): 
        self.startValue = num
        self.curValue = num
        self.isPlayersTurn = startingPlayer
        self.generateTree()
        self.minmax()

    def copy(self):
        newState = GameState()
        newState.startValue = self.startValue
        newState.curValue = self.curValue
        newState.isPlayersTurn = self.isPlayersTurn
        newState.botText = self.botText
        newState.lastBotAction = self.lastBotAction
        newState.lastHumanAction = self.lastHumanAction
        newState.lastAction = self.lastAction
        newState.children = []
        newState.parent = self
        newState.nodeValue = self.nodeValue
        return newState

    def generateTree(self):
        self.generateChildren()
        for childState in self.children:
            childState.generateTree()

    def generateChildren(self):
        for option in [5,6,11]:
            if self.checkTurnValidity(option) and self.curValue>10:
                childState = self.copy()
                if childState.isPlayersTurn:
                    childState.tree_HumanTurn(option)
                else:
                    childState.tree_BotTurn(option)
                self.children.append(childState)

    def tree_BotTurn(self, num): #metode koka veidošanai, kurā netiek izmantots algoritms, bet citi mainīgie mainīti tā, itkā būtu bijis bot gājiens
        self.subtract(num)
        self.lastAction = num
        self.lastBotAction = num
        self.botText = "Bot played " + str(num)
        self.isPlayersTurn = True

    def tree_HumanTurn(self, num):
        self.subtract(num)
        self.lastAction = num
        self.lastHumanAction = num
        self.isPlayersTurn = False

    def minmax(self):
        if self.children == []:
            self.calculate_EndNodeValue()
        else:
            self.calculate_innerNodeValue()
    def calculate_EndNodeValue(self):
        if self.isPlayersTurn:
            self.nodeValue = 0
        else: self.nodeValue = 1
    def calculate_innerNodeValue(self):
        if self.isPlayersTurn:  #vērtējumi no cilvēka skatupunkta - max = cilvēks uzvar
            minmax_func = max
        else:
            minmax_func = min
        children_Values = []
        for childState in self.children:
            if childState.nodeValue == None:
                childState.minmax()
            children_Values.append(childState.nodeValue)
        self.nodeValue = minmax_func(children_Values)

    def botTurn(self): #Maina koka "head state" uz pareizo zaru, atkarībā no bot gājiena
        minVal = 1
        for childState in self.children:
            if childState.nodeValue<minVal:
                minVal = childState.nodeValue
        for childState in self.children:
            if childState.nodeValue == minVal:
                return childState

    def humanTurn(self, num):  #Maina koka "head state" uz pareizo zaru, atkarībā no spēlētāja gājiena
        for childState in self.children:
            if childState.lastAction == num:
                return childState
        

    def subtract(self, num):
        self.curValue-=num

    def checkTurnValidity(self, num):
        if self.lastHumanAction==num and self.lastBotAction==num:
            return False
        else:
            return True