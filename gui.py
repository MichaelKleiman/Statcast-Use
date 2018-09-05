#!/usr/bin/python3.6
from tkinter import *
import os
import catcherArm
import sprintSpeed
import stddev
import scout
import percentile
import positionArray

#redraws all the frames so all subframes end up in the right place
def redraw():
    throwOptionsFrame.pack_forget()
    sprintOptionsFrame.pack_forget()
    topFrame.pack_forget()
    nextFrame.pack_forget()
    midFrame.pack_forget()
    midNextFrame.pack_forget()
    displayLabel.pack_forget()
    midMeanMedianFrame.pack_forget()
    if throwVar.get(): 
        throwOptionsFrame.pack(side = RIGHT)
    elif sprintVar.get():
        sprintOptionsFrame.pack(side = RIGHT)
    topFrame.pack()
    nextFrame.pack()
    midFrame.pack()
    if stddevVar.get() + scoutVar.get():
        midMeanMedianFrame.pack()
    midNextFrame.pack()
    if len(displayLabel['text']) > 0:
        displayLabel.pack()

#removes lowercase letters at the start of words, converts final 'jr', 'Jr', and 'jr.' to 'Jr.'
def handleName():
    name = entry.get()
    if name[0].islower():
        name = name[0].upper() + name[1:]
    i = name.index(' ')
    if name[i + 1].islower():
        name = name[0:i+1] + name[i+1].upper() + name[i+2:]
    if name[-3:] == 'jr.':
        name = name[0:-3] + 'Jr.'
    elif name [-2:] == 'jr' or name[-2:] == 'Jr':
        name = name[0:-2] + 'Jr.'
    return name
#displays a string. makes submit() a little cleaner
def display(string):
    displayLabel.pack()
    displayLabel['text'] = string

#when the button is clicked or return is pressed, runs the requested calculation from the imported files
#gets data from baseballsavant.mlb.com/...
def submit():
    b['state'] = DISABLED
    b.update()
    tup = catcherArm.main() if throwVar.get() else sprintSpeed.main()
    #get spring speed comparisons by position
    if sprintVar.get() and byPosVar.get() and not stddevVar.get():
        try:
            name = handleName()
            tup = positionArray.main(tup, name) 
        except:
            display('please enter a reasonably formatted name')
            b['state'] = NORMAL
            b.update()
            return
    index = 1 
    if throwVar.get():
        index = exchangeVar.get() + poptimeVar.get() + armStrengthVar.get() 
    if stddevVar.get():
        display(stddev.main(tup, None, index, meanVar.get()))
        b['state'] = NORMAL
        b.update()
        return
    try:
        name = handleName()
    except:
        display('please enter a reasonably formatted name')
        b['state'] = NORMAL
        b.update()
        return
    if percentileVar.get():
        if throwVar.get() and exchangeVar.get() + poptimeVar.get():
            display(percentile.main(tup, name, index, True))
        else: 
            display(percentile.main(tup, name, index))
        b['state'] = NORMAL
        b.update()
        return
    if throwVar.get() and (index == 1 or index == 4):
        display(scout.main(tup, name, index, meanVar.get(), True))
        b['state'] = NORMAL
        b.update()
        return
    display(scout.main(tup, name, index, meanVar.get()))
    b['state'] = NORMAL
    b.update()

#displays the textbox if the current calculation requiers a name, otherwise disables the textbox
def displayTextBox(boolean=True):
    if boolean:
        enterName.pack(side=LEFT)
        entry.pack(side=LEFT)
        entry['state'] = NORMAL 
        return
    entry['state'] = DISABLED 


#needs to modify behavior of Backspace for CTRL+Backspace combination.
#also determines if the current deletion will clear the text box (and thus need to disable the button)
#the normal Backspace event still happens afterwards
def handleBackspace():
    global ctrl
    global entryHasText
    if ctrl:
        try:
            x = entry.index(INSERT) - 1
            s = entry.get() 
            space = s[x] == ' '
            while (s[x] == ' ') == space:
                x -= 1
            
            entry.delete(x + 2, INSERT)
        except:
            entry.delete(0, INSERT)
            if len(entry.get()) == 0:
                entryHasText = False
                b['state'] = DISABLED
    b.update()
    return
    if len(entry.get()) == 1 and entry.index(INSERT) != 0:
        b['state'] = DISABLED
        entryHasText = False
        
    b.update()
    return 
#same as handleBackspace, but reversed and for the 'Delete' Key. Called by keyPress
def handleDelete():
    global ctrl
    global entryHasText
    if ctrl:
        try:
            x = entry.index(INSERT)
            s = entry.get() 
            space = s[x] == ' '
            while (s[x]== ' ') == space:
                x += 1
            entry.delete(INSERT, x - 1)
        except:
            entry.delete(INSERT, END)
            if len(entry.get()) == 0:
                entryHasText = False
                b['state'] = DISABLED
    b.update()
    return
    if len(entry.get()) == 1 and entry.index(INSERT) == 0:
        b['state'] = DISABLED
        entryHasText = False
        
    b.update()
    return 
    
#for knowing if left CTRL is currently pressed.
def controlPressed(event):
    global ctrl
    ctrl = True
def controlReleased(event):
    global ctrl
    ctrl = False

#makes ctrl+a delete the whole think, instead of jump to the left
def handlectrla(event):
   b['state'] = DISABLED
   global entryHasText
   entry.delete(0, END)
   entryHasText = False

#handles keypresses, except for left CTRL
def keyPress(event):
    if event.keysym == 'BackSpace':
        handleBackspace()
        return
    if event.keysym == 'Delete':
        handleDelete()
        return
    if event.keysym == 'Return' and b['state'] == NORMAL:
        submit()
        return
    global entryHasText
    
    global ctrl
    if ctrl and event.keysym == 'a':
        handlectrla(event)
        validate()
    elif not entryHasText:
        entryHasText = True
        validate()
         

#sets up the state of the window
#each conditional is to determine whether the button should be enabled or not
#one also checks if the textbox for entering names should be displayed
def validate():
    global entryHasText
    redraw()
    if throwVar.get() + sprintVar.get() == 0:
        b['state'] = DISABLED 
        displayTextBox(False) 
        b.update()
        return     
    if percentileVar.get() + stddevVar.get() + scoutVar.get() == 0:
        b['state'] = DISABLED 
        displayTextBox(False) 
        b.update()
        return
    
    if percentileVar.get() + scoutVar.get():
        displayTextBox()
        if not entryHasText: 
            b['state'] = DISABLED 
            b.update()
            return 
    else:
        displayTextBox(False)
    if meanVar.get() + medianVar.get() + percentileVar.get():
        b['state'] = NORMAL
        b.update()
        return
    b['state'] = DISABLED

#used by the functions below to set the other checkboxes to empty
def unset():
    percentileVar.set(0)
    stddevVar.set(0)
    scoutVar.set(0)
def unsetRightThrow():
   exchangeVar.set(0)
   armStrengthVar.set(0)
   poptimeVar.set(0)
   
#the functions below set the button for which they're named on, and the other ones in its group off
def sprint():
    sprintVar.set(1)
    throwVar.set(0)
    validate()
def throw():
    throwVar.set(1)
    sprintVar.set(0)
    validate()
def meanButton():
    meanVar.set(1)
    medianVar.set(0)
    validate()
def medianButton():
    medianVar.set(1)
    meanVar.set(0)
    validate()
def poptime():
    unsetRightThrow() 
    poptimeVar.set(1) 
    validate() 
def exchange():
    unsetRightThrow()
    exchangeVar.set(4)
    validate()
def armStrength():
    unsetRightThrow()
    armStrengthVar.set(3)
    validate()
def togglePercentile():
    unset()
    percentileVar.set(1)
    validate()
def toggleStddev():
    unset()
    stddevVar.set(1)
    validate()
def toggleScout():
    unset()
    scoutVar.set(1)
    validate()

#(mostly) global vars
throwVarLast = False
top = Tk()
top.resizable(False, False) #the window behaves erratically if it's been resized
ctrl = False
entryHasText = False
rightMenuThrow = False
throwVar = IntVar()
sprintVar = IntVar()
percentileVar = IntVar()
stddevVar = IntVar()
scoutVar = IntVar()
poptimeVar = IntVar()
poptimeVar.set(1)
exchangeVar = IntVar()
armStrengthVar = IntVar()
meanVar = IntVar()
medianVar = IntVar()
byPosVar = IntVar()
defaultFont = ('Times', '16')

#containers
topFrame = Frame(top)
nextFrame = Frame(top)
midFrame = Frame(top)
midMeanMedianFrame = Frame(top)
midMeanMedianSubFrame = Frame(midMeanMedianFrame)
midNextFrame = Frame(top)
throwOptionsFrame = Frame(top)
sprintOptionsFrame = Frame(top)
#content
sprint = Checkbutton(topFrame, command = sprint, text = 'sprint', font = defaultFont, variable = sprintVar, onvalue = 1, offvalue = 0)  
throw = Checkbutton(topFrame, command = throw, text = 'throwing', font = defaultFont, variable = throwVar, onvalue = 1, offvalue = 0)
percentileButton = Checkbutton(nextFrame, command = togglePercentile, text = 'percentile', font = defaultFont, variable = percentileVar, onvalue = 1, offvalue = 0)
stddevButton = Checkbutton(nextFrame, command = toggleStddev, text = 'stddev', font = defaultFont, variable = stddevVar, onvalue = 1, offvalue = 0)
scoutButton = Checkbutton(nextFrame, command = toggleScout, text = 'scout', font = defaultFont, variable = scoutVar, onvalue = 1, offvalue = 0)

poptimeButton = Checkbutton(throwOptionsFrame, command = poptime, text = 'poptime', font = defaultFont, variable = poptimeVar, onvalue = 1, offvalue = 0)
exchangeButton = Checkbutton(throwOptionsFrame, command = exchange, text = 'exchange time', font = defaultFont, variable = exchangeVar, onvalue = 4, offvalue = 0)
armStrengthButton = Checkbutton(throwOptionsFrame, command = armStrength, text = 'Arm Strength', font = defaultFont, variable = armStrengthVar, onvalue = 3, offvalue = 0)


rightThrowLabel = Label(throwOptionsFrame, font = defaultFont, text = 'select stat:')
rightSprintButton = Checkbutton(sprintOptionsFrame, font = defaultFont, text = 'by position?', variable = byPosVar, command = validate)
entry = Entry(midFrame, font = ('Times','13'), validate = 'key')
enterName = Label(midFrame, font = defaultFont, text = 'enter name:')
displayLabel = Label(top, font = defaultFont, padx = 5, wraplength = 380)
b = Button(midNextFrame, state = DISABLED, font = ('Times', '14'), text = 'go', command = submit)
quitButton = Button(midNextFrame, font = ('Times', '14'), text = 'exit', command = sys.exit)
spacer = Label(midNextFrame)

meanMedianLabel = Label(midMeanMedianFrame, font = ('Times', '14'), text = 'from the mean or the median?')
meanButton = Checkbutton(midMeanMedianSubFrame, font = ('Times', '14'), command = meanButton, text = 'mean', variable = meanVar)
medianButton = Checkbutton(midMeanMedianSubFrame, font = ('Times', '14'), command = medianButton, text = 'median', variable = medianVar)
#time to pack
meanMedianLabel.pack()
midMeanMedianSubFrame.pack()
meanButton.pack(side = LEFT)
medianButton.pack(side = RIGHT)

redraw()
sprint.pack(side = LEFT)
throw.pack(side = LEFT)

rightThrowLabel.pack(side = LEFT)
rightSprintButton.pack(side = LEFT)
poptimeButton.pack() 
armStrengthButton.pack()
exchangeButton.pack()

stddevButton.pack(side = LEFT, padx = 5)
percentileButton.pack(side = LEFT)
scoutButton.pack(side = LEFT, padx = 5)
quitButton.pack(side = LEFT)
spacer.pack(side = LEFT, padx=7)
b.pack(side = RIGHT)

entry.bind("<Key>", keyPress)
entry.bind("<KeyPress-Control_L>", controlPressed)
entry.bind("<KeyRelease-Control_L>", controlReleased)
frame = Frame(top)
frame.focus_set()
top.geometry("+0+0")
top.mainloop()

