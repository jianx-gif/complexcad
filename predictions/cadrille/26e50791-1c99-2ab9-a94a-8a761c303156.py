import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-47))
r=w0.sketch().circle(67).push([(37,11)]).circle(29,mode='s').finalize().extrude(2).union(w0.sketch().circle(100).circle(88,mode='s').finalize().extrude(67)).union(w0.sketch().segment((93,-12),(97,-12)).segment((97,14)).segment((93,14)).arc((94,1),(93,-12)).assemble().finalize().extrude(94))