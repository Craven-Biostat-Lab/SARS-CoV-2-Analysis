import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np

import sys, random
import TableAnalysis as ta

def attributesToKey(s, h, cl):
    return f"{s} {h} {cl}"

def setMatchArray(combinations):
    return [0 for _ in range(len(list(combinations.keys())))]

def updateMatchArray(ma, idx):
    ma[idx] = 1 # here the only possible values are 0 or 1
    return ma

def intToBinary(n, ln): # must be ln elements long
    if n == 0: return [0 for _ in range(ln)]
    ret = []
    while n > 0:
        ret = [n % 2] + ret
        n = n // 2
    return [0 for _ in range(ln - len(ret))] + ret

def binomRow(n):
    ret = [intToBinary(i, n) for i in range(2**n)]
    ret.reverse()
    return ret

def binaryToInt(b):
    factor = 1
    ret = 0
    for digit in b[::-1]:
        ret += digit * factor
        factor *= 2
    return ret

def generateColors(ta):
    ret = ["#FFFFFF"]
    random.seed()
    for _ in range(ta - 1):
        ret.append(f"#{'%06x' % random.randint(0, 0xFFFFFF)}")
    return ret

def main():
    # pulling data
    sym_col = 0 
    cell_col = 3
    hours_col = 4
    studies_col = 6

    proteins, cell_lines, hours, studies = [], [], [], []
    rows = ta.getRows("csv/schmidtflynnshererstandard_v2.csv")
    for row in rows[1:]:
        for dc in [[proteins, sym_col], [cell_lines, cell_col], [hours, hours_col], [studies, studies_col]]:
            if row[dc[1]].strip() not in dc[0]: dc[0].append(row[dc[1]].strip())

    # generating all possible attribute combinations (ACs)
    # pulling all attributes
    for i, thing in enumerate(hours):
        try: hours[i] = int(thing)
        except: hours[i] = 0

    cell_lines.sort()
    hours.sort()
    studies.sort()
    hours = [str(n) for n in hours]

    # combining them into ACs
    combinations = {}
    for s in studies:
        for h in hours:
            for cl in cell_lines:
                combinations[f"{s} {h} {cl}"] = False # Assume it's not found. True later if actually a used AC

    # remove any AC that isn't actually used
    for row in rows[1:]:
        combinations[f"{row[studies_col].strip()} {row[hours_col]} {row[cell_col]}"] = True

    actual_combos = {}
    for combo in combinations:
        if combinations[combo]: actual_combos[combo] = len(list(actual_combos.keys()))

    combinations = actual_combos

    # setting up arrays containing all matched ACs
    data = {}
    for p in proteins:
        data[p] = setMatchArray(combinations)

    # update each match array when AC is found
    for row in rows[1:]:
        idx = combinations[attributesToKey(row[studies_col].strip(), row[hours_col], row[cell_col])]
        data[row[sym_col]] = updateMatchArray(data[row[sym_col]], idx)

    # assuming n = number of used ACs, generate nCk combinations for each k = ACs used by a certain protein
    # we then order all proteins according to these generated combinations.
    poss_combos = binomRow(len(list(combinations.keys())))
    new_data = {}
    for combo in poss_combos:
        for key in data.keys():
            if data[key] == combo: 
                new_data[key] = data[key]

    # copying over this rearrangement to original data dictionary
    data = new_data

    # replacing all the 1's with cluster_id, so that each cluster has a unique color 
    # cluster_id just converts the series of 1's and 0's to decimal (binaryToInt()) to
    # assign itself a value.
    for key in data.keys():
        cluster_id = binaryToInt(data[key])
        new_values = [0 for _ in range(len(data[key]))]
        for i, entry in enumerate(data[key]):
            if entry != 0: new_values[i] = cluster_id
        data[key] = new_values

    # write this data out to a csv file so that seaborn can read it
    f = open("csv/heatmapdata_freq.csv", 'w')
    f.write(f"protein")
    for c in combinations.keys(): f.write(f",{c}")
    f.write("\n")

    for key in data.keys():
        f.write(key)
        for entry in data[key]: f.write(f",{entry}")
        f.write("\n")
    f.close()

    df = pd.read_csv("csv/heatmapdata_freq.csv", skiprows=1, index_col=0)

    fig, ax = plt.subplots()
    ax.set(
        xlabel="attribute combination (study/hour/cell line)", 
        ylabel="protein", 
        title="Protein frequency in various studies"
    )

    xticklabels = list(combinations.keys())
    yticklabels = list(data.keys())

    palette = sb.set_palette(generateColors(len(list(data.keys()))))

    sb.heatmap(
        df, 
        cmap=sb.color_palette(), 
        cbar=False, 
        xticklabels=xticklabels, 
        yticklabels=yticklabels,
    )

    plt.subplots_adjust(bottom=0.2)
    plt.ylabel("protein")
    plt.xlabel("attribute combination (study/hour/cell line)")
    plt.xticks(rotation=0)
    plt.title("Protein frequency in various studies")
    plt.show()

if __name__ == "__main__":
    main()
