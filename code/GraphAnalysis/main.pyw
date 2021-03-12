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

    try: # make the logo optional
        from PIL import Image, ImageTk

        logoFrame = tk.Frame(leftMasterFrame)
        logoFrame.pack(padx=10, side=tk.TOP)

        logo = Image.open("img/logo_small.png")
        logoTk = ImageTk.PhotoImage(logo)

        logoLabel = tk.Label(logoFrame, image=logoTk)
        logoLabel.pack()

    except ModuleNotFoundError: pass

    selectionFrame = tk.Frame(leftMasterFrame)
    selectionFrame.pack(padx=10, pady=20, side=tk.TOP)

    selectionTop = tk.Frame(selectionFrame)
    selectionLabel = tk.Label(selectionTop, text="Select identifier", font="TkDefaultFont 10 bold")
    selectionLabel.pack(side=tk.LEFT)
    selectionTop.pack()

    selectionMid = tk.Frame(selectionFrame)
    selectionSelectLabel = tk.Label(selectionMid, text="Identifier: ")
    selectionSelectLabel.pack(side=tk.LEFT)
    selectionSelectEntry = tk.Entry(selectionMid, width=12, font="TkFixedFont")
    selectionSelectEntry.pack(side=tk.LEFT)
    selectionMid.pack()

    selectionBot = tk.Frame(selectionFrame)
    selectionBotLeft = tk.Frame(selectionBot)
    selectionBotRight = tk.Frame(selectionBot)

    selectionDegreeLabel = tk.Label(selectionBotLeft, text="Max distance: ")
    selectionDegreeLabel.pack(side=tk.TOP)
    
    degreeEntry = tk.Entry(selectionBotRight, width=4, font="TkFixedFont")
    degreeEntry.pack(side=tk.TOP)

    neighborsLabel = tk.Label(selectionBotLeft, text="Max neighbors: ")
    neighborsLabel.pack(side=tk.TOP)

    neighborsEntry = tk.Entry(selectionBotRight, width=4, font="TkFixedFont")
    neighborsEntry.pack(side=tk.TOP)

    selectionBotLeft.pack(side=tk.LEFT)
    selectionBotRight.pack(side=tk.LEFT)

    ## DISPLAYING RESULTS
    # declare this up here so graphData() can work with elements involved

    resultsFrame = tk.Frame(top)
    resultsMiddle = tk.Frame(resultsFrame)
    resultsScrollbar = tk.Scrollbar(resultsMiddle)
    resultsText = tk.Text(resultsMiddle, height=30, width=45, yscrollcommand=resultsScrollbar.set, font="TkFixedFont")

    selectionBot2 = tk.Frame(selectionFrame)
    alphaTicked = tk.IntVar()
    orderCheckbox = tk.Checkbutton(selectionBot2, variable=alphaTicked, text="Order alphabetically", onvalue=1, offvalue=0)
    orderCheckbox.select()

    selectionBot3 = tk.Frame(selectionFrame)
    limitTicked = tk.IntVar()
    limitCheckbox = tk.Checkbutton(selectionBot3, variable=limitTicked, text="Limit starting neighbors", onvalue=1, offvalue=0)
    limitCheckbox.pack()

    resultsBarFrame = tk.Frame(resultsFrame)
    progress = ttk.Progressbar(resultsBarFrame, orient=tk.HORIZONTAL, length=100)
    progress.pack(ipadx=100)

    selectionMostBottom = tk.Frame(selectionFrame)
    generateButtonStr = tk.StringVar()
    generateButtonStr.set("Generate graph!")
    generateButton = tk.Button(selectionMostBottom, text="Generate graph!", command=(lambda: gh.startThread(
        data,
        selectionSelectEntry.get(), 
        degreeEntry.get(),
        neighborsEntry.get(),
        resultsText,
        alphaTicked.get(),
        limitTicked.get(),
        generateButton,
        progress
    )))
    generateButton.pack(side=tk.LEFT)
    selectionBot.pack()

    orderCheckbox.pack(side=tk.LEFT)
    selectionBot2.pack()
    selectionBot3.pack()
    selectionMostBottom.pack()

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

    resultsError = tk.Frame(resultsFrame)
    resultsErrorVar = tk.StringVar()
    resultsErrorVar.set("\n")
    resultsErrorDisp = tk.Label(resultsError, textvariable=resultsErrorVar)
    resultsErrorDisp.pack()

    resultsBottom = tk.Frame(resultsFrame)
    resultsCSVButton = tk.Button(resultsBottom, text="Output to .csv", command=(lambda: op.outputToCSV(data)))
    resultsCSVButton.pack(side=tk.LEFT)
    resultsCytoButton = tk.Button(resultsBottom, text="Output to Cytoscape", command=(lambda: op.startCytoscapeThread(
        data,
        resultsErrorVar,
        resultsCytoButton
    )))

    resultsCytoButton.pack(side=tk.LEFT)
    resultsBarFrame.pack()
    resultsBottom.pack()
    resultsError.pack()

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

    jumpToSymbolEntry = tk.Entry(jumpToSymbolFrame, width=12, font="TkFixedFont")
    jumpToSymbolEntry.pack(side=tk.LEFT)

    jumpToLayerFrame = tk.Frame(jumpToFrame)
    jumpToLayerFrame.pack(side=tk.TOP)

    jumpToLayerLabel = tk.Label(jumpToLayerFrame, text="In layer: ")
    jumpToLayerLabel.pack(side=tk.LEFT)

    jumpToLayerEntry = tk.Entry(jumpToLayerFrame, width=4, font="TkFixedFont")
    jumpToLayerEntry.pack(side=tk.LEFT)

    """
    jumpToLayerOptions = ["First layer", "Second layer", "Viral interactions"]
    jumpToLayerOptionsVar = tk.StringVar()
    jumpToLayerOptionsVar.set(jumpToLayerOptions[0])

    jumpToLayerOptionsMenu = tk.OptionMenu(jumpToLayerFrame, jumpToLayerOptionsVar, *jumpToLayerOptions)
    jumpToLayerOptionsMenu.pack(side=tk.LEFT)
    """

    jumpStatus = tk.StringVar()
    jumpStatus.set("")
    jumpStatusLabel = tk.Label(jumpToFrame, textvariable=jumpStatus)

    # adding space between layer entry and go button...of course this is optimal wym
    jumpToPadding = tk.Label(jumpToLayerFrame, text=" ")
    jumpToPadding.pack(side=tk.LEFT)

    jumpToGoButton = tk.Button(jumpToLayerFrame, text="Go!", command=(lambda: sc.scrollTo(
        data,
        jumpStatus,
        jumpToSymbolEntry.get(),
        jumpToLayerEntry.get(),
        resultsText,
        resultsScrollbar
    )))
    jumpToGoButton.pack(side=tk.LEFT)
    jumpStatusLabel.pack(side=tk.TOP)

    top.mainloop()

if __name__ == "__main__":
    main()