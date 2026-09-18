import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().segment((-87,-11),(87,11)).arc((0,78),(-87,11)).assemble().finalize().extrude(-200).union(w0.sketch().arc((-4,-99),(3,-81),(13,-65)).arc((-19,18),(87,19)).arc((79,54),(61,83)).arc((-59,33),(-4,-99)).assemble().finalize().extrude(-183))