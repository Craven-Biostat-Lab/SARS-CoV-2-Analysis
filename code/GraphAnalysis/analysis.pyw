import tkinter as tk
from tkinter import Scrollbar
from tkinter import ttk

import csvhandling as ch

def main():
    top = tk.Tk()
    top.title("BioGRID Analysis Tool")
    top.resizable(False, False)
    #top.geometry("500x280")

    stepOneAndTwoFrame = tk.Frame(top)
    stepOneAndTwoFrame.pack(side=tk.LEFT)

    ## STEP TWO

    data = ch.Data()
    data.set("csv/allhumanproteininteractions_v1.csv")
    ch.extractData(
        data.get(),
        "B",
        "E",
        "1",
        data
    )

    stepTwoFrame = tk.Frame(stepOneAndTwoFrame)
    stepTwoFrame.pack(padx=10, pady=20, side=tk.TOP)
    
    ## Top section

    stepTwoTop = tk.Frame(stepTwoFrame)
    stepTwoLabel = tk.Label(stepTwoTop, text="Step one: select identifier", font="TkDefaultFont 10 bold")
    stepTwoLabel.pack(side=tk.LEFT)
    stepTwoTop.pack()

    stepTwoMid = tk.Frame(stepTwoFrame)
    stepTwoSelectLabel = tk.Label(stepTwoMid, text="Enter symbol: ")
    stepTwoSelectLabel.pack(side=tk.LEFT)
    stepTwoSelectEntry = tk.Entry(stepTwoMid, width=16, font="TkFixedFont")
    stepTwoSelectEntry.pack(side=tk.LEFT)
    stepTwoMid.pack()

    stepTwoBot = tk.Frame(stepTwoFrame)
    stepTwoDegreeLabel = tk.Label(stepTwoBot, text="Max distance: ")
    stepTwoDegreeLabel.pack(side=tk.LEFT)
    
    degreeOptions = ["1", "2"]
    degreeOptionsVar = tk.StringVar()
    degreeOptionsVar.set(degreeOptions[0])

    degreeOptionsMenu = tk.OptionMenu(stepTwoBot, degreeOptionsVar, *degreeOptions)
    degreeOptionsMenu.pack(side=tk.LEFT)

    # declare this up here so graphData() can work with elements involved
    stepThreeFrame = tk.Frame(top) # holds step one: importing data
    stepThreeMiddle = tk.Frame(stepThreeFrame)
    stepThreeScrollbar = tk.Scrollbar(stepThreeMiddle)
    stepThreeText = tk.Text(stepThreeMiddle, height=15, width=45, yscrollcommand=stepThreeScrollbar.set, font="TkFixedFont")

    stepTwoBot2 = tk.Frame(stepTwoFrame)
    isTicked = tk.IntVar()
    orderCheckbox = tk.Checkbutton(stepTwoBot2, variable=isTicked, text="Order alphabetically", onvalue=1, offvalue=0)
    orderCheckbox.select()

    generateButtonStr = tk.StringVar()
    generateButtonStr.set("Generate graph!")
    generateButton = tk.Button(stepTwoBot, text="Generate graph!", command=(lambda: ch.graphData(
        data,
        stepTwoSelectEntry.get(), 
        degreeOptionsVar.get(),
        stepThreeText,
        isTicked.get()
    )))
    generateButton.pack(side=tk.LEFT)
    stepTwoBot.pack()

    orderCheckbox.pack(side=tk.LEFT)
    stepTwoBot2.pack()

    ## STEP THREE

    stepThreeFrame.pack(padx=10, pady=20, side=tk.RIGHT)
    
    ## Top section

    stepThreeTop = tk.Frame(stepThreeFrame)
    stepThreeLabel = tk.Label(stepThreeTop, text="Step two: results", font="TkDefaultFont 10 bold")
    stepThreeLabel.pack(side=tk.TOP)
    stepThreeHelp = tk.Label(stepThreeTop, text="identifierA interacts with (>>) identifierB", font="TkDefaultFont 10 italic")
    stepThreeHelp.pack(side=tk.TOP)
    stepThreeTop.pack()
    
    # stepThreeScrollBar declared above 
    stepThreeScrollbar.config(command=stepThreeText.yview)
    stepThreeScrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    stepThreeText.pack(side=tk.LEFT)
    stepThreeMiddle.pack()

    stepThreeBottom = tk.Frame(stepThreeFrame)
    stepThreeCSVButton = tk.Button(stepThreeBottom, text="Find viral interactions and output to .csv", command=(lambda: ch.outputToCSV(data)))
    stepThreeCSVButton.pack(side=tk.LEFT)
    """
    stepThreeCytoButton = tk.Button(stepThreeBottom, text="Output to Cytoscape", command=(lambda: ch.outputToCytoscape(data)))
    stepThreeCytoButton.pack(side=tk.LEFT)
    """
    stepThreeBottom.pack()

    generateButton.config(text="Generate graph!")
    top.mainloop()

if __name__ == "__main__":
    main()