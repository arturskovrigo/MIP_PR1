import tkinter as tk
from tkinter import messagebox
import GameState

class GameMain:   #Galvenā spēli aprakstošā klase
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("400x350")   #Loga izmērs
        self.root.title("PR1")
        self.startVal_var = tk.IntVar(value = 70)   #Noklusējuma sākuma vērtība
        self.startPlayer_var  = tk.BooleanVar(self.root, True)  #Noklusējuma sākuma spēlētājs

    def preGameWindow(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.startValueLabel = tk.Label(self.root, text = "Start value")
        self.startPlayerLabel = tk.Label(self.root, text = "Starting player")
        
        self.startValueTextBox = tk.Entry(self.root, width = 30, textvariable = self.startVal_var)

        self.radioYou = tk.Radiobutton(self.root, text = "You",
                                      variable=self.startPlayer_var, value = True)
        self.radioBot = tk.Radiobutton(self.root, text = "Bot",
                                      variable=self.startPlayer_var, value = False)
        self.startButton = tk.Button(self.root, text = "Start", bd = '5',
                                command = self.startGame)
        self.stopButton = tk.Button(self.root, text = "Stop", bd = '5',
                                command = self.root.destroy)
        self.startValueLabel.pack()
        self.startValueTextBox.pack()
        self.startPlayerLabel.pack()
        self.radioYou.pack()
        self.radioBot.pack()
        self.startButton.pack()
        self.stopButton.pack()

    def startGame(self):
        self.state = GameState.GameState()
        self.state.submit(self.startVal_var.get(), self.startPlayer_var.get())
        if self.state.isPlayersTurn==False:
            self.state = self.state.botTurn()
        self.startValueLabel.pack_forget()
        self.startPlayerLabel.pack_forget()
        self.radioYou.pack_forget()
        self.radioBot.pack_forget()
        self.startValueTextBox.pack_forget()
        self.startButton.pack_forget()
        self.stopButton.pack_forget()

        self.firstTurn()

    def subtract(self, subtractNum):
        if self.state.checkTurnValidity(subtractNum):
            self.state = self.state.humanTurn(subtractNum)
            if self.state.curValue<=10:     #spēle beidzas, ja gala vērtība iz mazāka, vai vienāda ar 10
                self.finishGame("You")
            self.state = self.state.botTurn()
            self.currentValue.config(text = str(self.state.curValue))
            self.botMoveLabel.config(text = self.state.botText)
            if self.state.curValue<=10:
                self.finishGame("Bot")
        else:
            messagebox.showwarning("Warning", "Cannot repeat the same move 2 times in a row")

    def finishGame(self, winnerStr):
        self.endWindow = tk.Toplevel(self.root)
        self.endWindow.title("Game end")
        self.endWindow.geometry("200x120")
        tk.Label(self.endWindow,
            text ="Game finished, " + winnerStr + " won").pack()
        end_startButton = tk.Button(self.endWindow, text = "New game", bd = 5, command=lambda: self.newGame(True))
        end_startButton.pack()
        end_stopButton = tk.Button(self.endWindow, text = "close", bd = 5, command=self.root.destroy)
        end_stopButton.pack()

    def newGame(self, is_endWindow = False):
        if is_endWindow:
            self.endWindow.destroy()
        self.botMoveLabel.pack_forget()
        self.currentValueLabel.pack_forget()
        self.currentValue.pack_forget()
        self.startButton.pack_forget()
        self.stopButton.pack_forget()
        self.btn3.pack_forget()
        self.btnClose.pack_forget()
        self.preGameWindow()

    def firstTurn(self):
        self.root.geometry("400x200")
        self.botMoveLabel = tk.Label(self.root, text = self.state.botText)
        self.currentValueLabel = tk.Label(self.root, text ="Current value")
        self.currentValue = tk.Label(self.root, text = str(self.state.curValue))
        self.startButton = tk.Button(self.root,
                            text = '- 5', bd = '5',
                            command = lambda: self.subtract(5))
        self.stopButton = tk.Button(self.root,
                            text = '- 6', bd = '5',
                            command = lambda: self.subtract(6))
        self.btn3 = tk.Button(self.root,
                            text = '- 11', bd = '5',
                            command = lambda: self.subtract(11))
        self.btnClose = tk.Button(self.root,
                            text = 'Back to menu', bd = 5,
                            command = self.newGame)
        self.botMoveLabel.pack()
        self.currentValueLabel.pack()
        self.currentValue.pack()
        self.startButton.pack()
        self.stopButton.pack()
        self.btn3.pack()
        self.btnClose.pack()


    