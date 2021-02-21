import numpy as np

def outputToCSV(d):
    if d.disp == "" or d.disp == "Identifier not found.": return

    w = open(f"results/{d.selected}_{d.layerCount}layer.csv", 'w')
    w.write(f"interactorA,interactorB,interactionType\n")

    for interaction in d.interactions:
        w.write(f"{interaction[0]},{interaction[1]},{interaction[2]}\n")

    w.close()

def outputToCytoscape(d, error):
    # d: data object
    # error: StringVar holding possible error

    if d.disp == "" or d.disp == "Identifier not found.": return

    try:
        from py2cytoscape.data.cyrest_client import CyRestClient
        import requests
        import json
    
    except ModuleNotFoundError: 
        error.set("ModuleNotFoundError: missing\nnecessary prerequisites.")
        return

    try: 
        cy = CyRestClient()
        cy.session.delete() # contentious?
        network = cy.network.create(name=f"{d.selected}_{d.layerCount}layer", collection="{d.selected} protein analysis")

    except requests.exceptions.ConnectionError:
        error.set("Cytoscape must be running in the\nbackground for this to work!")
        return

    except UnboundLocalError:
        error.set("Cytoscape must be running in the\nbackground for this to work!")
        return