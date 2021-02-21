def scrollTo(d, e, s, l, txt, scrollbar):
    # d: data object
    # e: StringVar showing error
    # s: symbol to jump to
    # l: layer selected ("First layer", "Second layer", or "Viral interactions")
    # txt: tkinter Text widget to adjust
    # scrollbar: tkinter Scrollbar to adjust

    # comb for the symbol in question
    lines = d.disp.split("\n")[:-1]
    lineCount = len(lines)
    currentLayer = False
    found = False
    position = 0.0

    dropDownTranslations = {
        "## ONE DEGREE OF SEPARATION:": "First Layer",
        "## TWO DEGREES OF SEPARATION:": "Second layer",
        "## VIRAL INTERACTIONS:": "Viral interactions"
    }
    
    # if searching in first layer
    if l == "First layer":
        if s == d.selected: found = True
        for i, line in enumerate(lines):
            if len(line.split()) == 0: continue
            term = line.split()[0]
            
            if term == "##": 
                if i == 0: continue     # skip past first header
                else: break             # stop at the next

            if line.split()[2].strip() == s:
                position = i / lineCount if i != 0 else 0.0
                e.set("")
                found = True
                break

    # if searching in second layer
    elif l == "Second layer":
        if len(d.layers[2]) == 0:   # check if we can even do this
            e.set("Layer out of bounds.")
            return

        for i, line in enumerate(lines):
            if len(line.split()) == 0: continue
            term = line.split()[0]
            
            if term == "##": currentLayer = dropDownTranslations[line]
            if currentLayer == l:   # if we're in the right layer,
                if term == s:       # and the first term in the line is the protein we're looking for,
                    position = i / lineCount if i != 0 else 0.0
                    e.set("")
                    found = True
                    break

    # if searching in viral layer
    else:
        for i, line in enumerate(lines):
            if len(line.split()) == 0: continue
            term = line.split()[0]
            
            if term == "##": currentLayer = dropDownTranslations[line]
            if currentLayer == l:   # if we're in the right layer,
                if term == s:       # and the first term in the line is the protein we're looking for,
                    position = i / lineCount if i != 0 else 0.0
                    e.set("")
                    found = True
                    break

    if not found:
        e.set("Identifier not found at layer specified.")
        return

    # now scroll to the actual location
    try: txt.yview_moveto(position - (1 / lineCount))
    except ZeroDivisionError: return