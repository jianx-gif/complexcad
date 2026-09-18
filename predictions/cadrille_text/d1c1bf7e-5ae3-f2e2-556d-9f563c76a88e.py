import cadquery as cq
w0=cq.Workplane('XY',origin=(-57,0,-100))
w1=cq.Workplane('XY',origin=(-57,0,-60))
r=w0.sketch().segment((26,-58),(57,-58)).segment((57,-28)).arc((42,-44),(26,-58)).assemble().finalize().extrude(200).union(w1.workplane(offset=160/2).moveTo(0,1).cylinder(160,3))