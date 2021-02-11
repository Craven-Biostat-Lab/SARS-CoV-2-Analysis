def outputToCSV(d):
    if d.disp == "" or d.disp == "Identifier not found.": return

    w = open(f"results/{d.selected}_{d.layerCount}layer.csv", 'w')
    w.write(f"interactorA,interactorB,interactionType\n")

    for interaction in d.interactions:
        w.write(f"{interaction[0]},{interaction[1]},{interaction[2]}\n")

    w.close()

def outputToCytoscape(d):
    print("Outputting to Cytoscape.")