import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,23))
r=w0.sketch().push([(-5,0)]).rect(190,118).rect(180,110,mode='s').finalize().extrude(-48).union(w0.sketch().segment((98,-12),(98,-11)).segment((99,-11)).arc((91,11),(98,-12)).assemble().finalize().extrude(2))