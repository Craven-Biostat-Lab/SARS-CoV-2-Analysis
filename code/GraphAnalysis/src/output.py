import numpy as np
import threading

def outputToCSV(d):
    if d.disp == "" or d.disp == "Identifier not found.": return

    filename = f"results/{d.selected}_{d.layerCount}L_{d.neighborCount}N"
    if d.headLimited == 0: filename += ".csv"
    else: filename += "_HL.csv"

    w = open(filename, 'w')
    w.write(f"interactorA,interactorB,interactorAType,interactorBType,layer,interactionType\n")

    for interaction in d.interactions:
        w.write(f"{interaction[0]},{interaction[1]},{interaction[2]},{interaction[3]},{interaction[4]},{interaction[5]}\n")

    w.close()

def outputToCytoscape(d, error, b):
    # d: data object
    # error: StringVar holding possible error

    if d.disp == "" or d.disp == "Identifier not found.": return
    b["state"] = "disabled"
    error.set("Processing Cytoscape request...\n")

    # declare filename here in case user hasn't yet outputted to .csv
    filename = f"results/{d.selected}_{d.layerCount}L_{d.neighborCount}N"
    if d.headLimited == 0: filename += ".csv"
    else: filename += "_HL.csv"

    try:
        from py2cytoscape.data.cyrest_client import CyRestClient
        import requests
        import json
    
    except ModuleNotFoundError: 
        error.set("ModuleNotFoundError: missing\nnecessary prerequisites.")
        b["state"] = "active"
        return

    try: 
        cy = CyRestClient()
        #cy.session.delete() # contentious?
        network = cy.network.create(name=filename, collection=f"{d.selected} protein analysis")

    except requests.exceptions.ConnectionError:
        error.set("Cytoscape must be running in the\nbackground for this to work!")
        b["state"] = "active"
        return

    except UnboundLocalError:
        error.set("Cytoscape must be running in the\nbackground for this to work!")
        b["state"] = "active"
        return

    except json.decoder.JSONDecodeError:
        error.set("Attempted too early, so the server\nwasn't ready. Please try again.")
        b["state"] = "active"
        return

    # begin adding nodes if connection to Cytoscape is not erroneous

    # adding human proteins involved
    for n in d.used:
        network.add_node(n)

    # adding SARS-CoV-2 proteins involved
    for v in d.viralUsed:
        network.add_node(v)

    df_network = network.get_node_table()
    for e in d.interactions:
        try:
            network.add_edge(
                list(df_network[df_network.name==e[0]]['SUID'])[0], 
                list(df_network[df_network.name==e[1]]['SUID'])[0], 
                directed=False
            )

        except IndexError: print(f"Index error at {e[0]}->{e[1]}.")

    # rearranging nodes into a circle, since this doesn't seem terribly intensive on the machine
    cy.layout.apply(name="circular", network=network)

    # reenable button if all goes well
    b["state"] = "active"
    error.set("\n")

def startCytoscapeThread(d, error, b):
    # use threading here since the Cytoscape thing can cause hanging
    th = threading.Thread(target=(lambda: outputToCytoscape(d, error, b)), daemon=True)
    th.start()