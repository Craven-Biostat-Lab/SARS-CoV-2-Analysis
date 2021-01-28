import csvhandling as ch

cols = ch.getCols(ch.getRows("csv/biogrid_3study_standard_v3.csv"))

v = set()
for thing in cols[3][1:]:
    v.add(thing)

print(v)
print(len(list(v)))