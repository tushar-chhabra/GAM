#!/usr/bin/env python
import re

reactions_file = "./reaction"

with open(reactions_file) as f:
    text = "".join(f.readlines())

def get_compound(s):
    return s.split()[-1]

def compounds(s):
    s = re.sub("\(.*?\)", "n", s)
    return map(get_compound, s.split("+"))

descriptions = text.split("///\n")

m2m = ["met.x\trxn\tmet.y"]
r2e = ["rxn\tenz"]

r2name = ["rxn\tname"]

for description in descriptions:
    if description == "":
        continue
    lines = description.split("\n")
    shift = 12
    last_name = None
    d = {}
    for line in lines:
        if line == "":
            continue
        name = line[:shift].strip()
        value = line[shift:]
        if name == "":
            name = last_name

        if name in d:
            d[name] += "\n" + value
        else:
            d[name] = value

        last_name = name

    rxn_id = d["ENTRY"].split()[0]

    if not "ENZYME" in d:
        d["ENZYME"] = ""

    enzymes = d["ENZYME"].split()
    r2e.extend(["%s\t%s" % (rxn_id, enzyme) for enzyme in enzymes])

    equation = d["EQUATION"]

    (left, right) = map(compounds, equation.split("<=>"))
    m2m.extend(["%s\t%s\t%s" % (c1, rxn_id, c2) for c1 in left for c2 in right])
    if "NAME" in d:
        r2name.append('%s\t"%s"' % (rxn_id, d["NAME"].split("\n")[0]))

with open("net.sif", "w") as f:
    f.write("%s\n" % "\n".join(m2m))

with open("rxn2enz.tsv", "w") as f:
    f.write("%s\n" % "\n".join(r2e))

with open("rxn2name.tsv", "w") as f:
    f.write("%s\n" % "\n".join(r2name))