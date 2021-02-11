import tkinter as tk
from tkinter import Scrollbar
from tkinter import ttk

from src import csvhandling as ch
from src import graph as gh
from src import output as op
from src import scroll as sc

def main():
    top = tk.Tk()
    top.title("Protein Analysis Tool")
    top.resizable(False, False)

    leftMasterFrame = tk.Frame(top)
    leftMasterFrame.pack(side=tk.LEFT)

    data = ch.Data()
    data.set("src/csv/allhumanproteininteractions_v1.csv")
    ch.extractData(
        data.get(),
        "B",
        "E",
        "1",
        data
    )

    ## SELECTING THE PROTEIN

    selectionFrame = tk.Frame(leftMasterFrame)
    selectionFrame.pack(padx=10, pady=20, side=tk.TOP)

    selectionTop = tk.Frame(selectionFrame)
    selectionLabel = tk.Label(selectionTop, text="Select identifier", font="TkDefaultFont 10 bold")
    selectionLabel.pack(side=tk.LEFT)
    selectionTop.pack()

    selectionMid = tk.Frame(selectionFrame)
    selectionSelectLabel = tk.Label(selectionMid, text="Enter symbol: ")
    selectionSelectLabel.pack(side=tk.LEFT)
    selectionSelectEntry = tk.Entry(selectionMid, width=16, font="TkFixedFont")
    selectionSelectEntry.pack(side=tk.LEFT)
    selectionMid.pack()

    selectionBot = tk.Frame(selectionFrame)
    selectionDegreeLabel = tk.Label(selectionBot, text="Max distance: ")
    selectionDegreeLabel.pack(side=tk.LEFT)
    
    degreeOptions = ["1", "2"]
    degreeOptionsVar = tk.StringVar()
    degreeOptionsVar.set(degreeOptions[0])

    degreeOptionsMenu = tk.OptionMenu(selectionBot, degreeOptionsVar, *degreeOptions)
    degreeOptionsMenu.pack(side=tk.LEFT)

    ## DISPLAYING RESULTS
    # declare this up here so graphData() can work with elements involved

    resultsFrame = tk.Frame(top)
    resultsMiddle = tk.Frame(resultsFrame)
    resultsScrollbar = tk.Scrollbar(resultsMiddle)
    resultsText = tk.Text(resultsMiddle, height=30, width=45, yscrollcommand=resultsScrollbar.set, font="TkFixedFont")

    selectionBot2 = tk.Frame(selectionFrame)
    isTicked = tk.IntVar()
    orderCheckbox = tk.Checkbutton(selectionBot2, variable=isTicked, text="Order alphabetically", onvalue=1, offvalue=0)
    orderCheckbox.select()

    generateButtonStr = tk.StringVar()
    generateButtonStr.set("Generate graph!")
    generateButton = tk.Button(selectionBot, text="Generate graph!", command=(lambda: gh.graphData(
        data,
        selectionSelectEntry.get(), 
        degreeOptionsVar.get(),
        resultsText,
        isTicked.get()
    )))
    generateButton.pack(side=tk.LEFT)
    selectionBot.pack()

    orderCheckbox.pack(side=tk.LEFT)
    selectionBot2.pack()

    resultsFrame.pack(padx=10, pady=20, side=tk.RIGHT)
    
    ## Top section

    resultsTop = tk.Frame(resultsFrame)
    resultsLabel = tk.Label(resultsTop, text="Results", font="TkDefaultFont 10 bold")
    resultsLabel.pack(side=tk.TOP)
    resultsHelp = tk.Label(resultsTop, text="identifierA interacts with (>>) identifierB", font="TkDefaultFont 10 italic")
    resultsHelp.pack(side=tk.TOP)
    resultsTop.pack()
    
    # resultsScrollBar declared above 
    resultsScrollbar.config(command=resultsText.yview)
    resultsScrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    resultsText.pack(side=tk.LEFT)
    resultsMiddle.pack()

    resultsBottom = tk.Frame(resultsFrame)
    resultsCSVButton = tk.Button(resultsBottom, text="Output to .csv", command=(lambda: op.outputToCSV(data)))
    resultsCSVButton.pack(side=tk.LEFT)
    resultsCytoButton = tk.Button(resultsBottom, text="Output to Cytoscape", command=(lambda: op.outputToCytoscape(data)))
    resultsCytoButton.pack(side=tk.LEFT)
    resultsBottom.pack()

    generateButton.config(text="Generate graph!")

    ## JUMP TO STUFF
    # declared down here so it can refer to elements from displayed results, defined earlier

    jumpToFrame = tk.Frame(leftMasterFrame)
    jumpToFrame.pack(padx=10, pady=10, side=tk.TOP)

    jumpToHeader = tk.Label(jumpToFrame, text="Jump to...", font="TkDefaultFont 10 bold")
    jumpToHeader.pack(side=tk.TOP)

    jumpToSymbolFrame = tk.Frame(jumpToFrame)
    jumpToSymbolFrame.pack(side=tk.TOP)

    jumpToSymbolLabel = tk.Label(jumpToSymbolFrame, text="Identifier: ")
    jumpToSymbolLabel.pack(side=tk.LEFT)

    jumpToSymbolEntry = tk.Entry(jumpToSymbolFrame, width=16, font="TkFixedFont")
    jumpToSymbolEntry.pack(side=tk.LEFT)

    jumpToLayerFrame = tk.Frame(jumpToFrame)
    jumpToLayerFrame.pack(side=tk.TOP)

    jumpToLayerLabel = tk.Label(jumpToLayerFrame, text="In: ")
    jumpToLayerLabel.pack(side=tk.LEFT)

    jumpToLayerOptions = ["First layer", "Second layer", "Viral interactions"]
    jumpToLayerOptionsVar = tk.StringVar()
    jumpToLayerOptionsVar.set(jumpToLayerOptions[0])

    jumpToLayerOptionsMenu = tk.OptionMenu(jumpToLayerFrame, jumpToLayerOptionsVar, *jumpToLayerOptions)
    jumpToLayerOptionsMenu.pack(side=tk.LEFT)

    jumpStatus = tk.StringVar()
    jumpStatus.set("")
    jumpStatusLabel = tk.Label(jumpToFrame, textvariable=jumpStatus)

    jumpToGoButton = tk.Button(jumpToLayerFrame, text="Go!", command=(lambda: sc.scrollTo(
        data,
        jumpStatus,
        jumpToSymbolEntry.get(),
        jumpToLayerOptionsVar.get(),
        resultsText,
        resultsScrollbar
    )))
    jumpToGoButton.pack(side=tk.LEFT)
    jumpStatusLabel.pack(side=tk.TOP)

    top.mainloop()

if __name__ == "__main__":
    main()