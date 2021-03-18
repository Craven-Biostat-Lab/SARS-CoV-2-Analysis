def scrollTo(d, e, s, l, txt, scrollbar):
    # d: data object
    # e: StringVar showing error
    # s: symbol to jump to
    # l: layer selected (now an entry widget)
    # txt: tkinter Text widget to adjust
    # scrollbar: tkinter Scrollbar to adjust

    # comb for the symbol in question
    lines = d.disp.split("\n")[:-1]
    lineCount = len(lines)
    currentLayer = False
    found = False
    position = 0.0

    try: 
        if l.lower()[0] == "v":
            l = d.layerCount + 1

        else: 
            l = int(l)

    except ValueError: e.set("Invalid layer selected.")

    # if searching in first layer
    if l == 1:
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

    # if searching in viral layer
    elif l == (d.layerCount + 1):
        for i, line in enumerate(lines):
            if len(line.split()) == 0: continue
            term = line.split()[0]
            
            if term == "##" and line.split()[1] == "VIRAL": 
                currentLayer = d.layerCount + 1

            if currentLayer == l:   # if we're in the right layer,
                if term == s:       # and the first term in the line is the protein we're looking for,
                    position = i / lineCount if i != 0 else 0.0
                    e.set("")
                    found = True
                    break

    # if in any other layer
    else:
        if len(d.layers[2]) == 0:   # check if we can even do this
            e.set("Layer out of bounds.")
            return

        for i, line in enumerate(lines):
            if len(line.split()) == 0: continue
            term = line.split()[0]
            
            if term == "##":
                try: currentLayer = int(line.split()[-1][0])
                except ValueError: continue # this happens when it gets to viral later

            if currentLayer == l:   # if we're in the right layer,
                if term == s:       # and the first term in the line is the protein we're looking for,
                    position = i / lineCount if i != 0 else 0.0
                    e.set("")
                    found = True
                    break

    if not found:
        e.set("Identifier not found.")
        return

    # now scroll to the actual location
    try: txt.yview_moveto(position - (1 / lineCount))
    except ZeroDivisionError: return