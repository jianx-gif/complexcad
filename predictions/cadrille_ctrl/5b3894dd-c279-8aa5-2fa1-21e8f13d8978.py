import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,20,0))
r=w0.sketch().segment((-1,-1),(1,-1)).segment((1,1)).segment((0,1)).arc((0,0),(-1,-1)).assemble().finalize().extrude(-80).union(w0.sketch().circle(35).push([(16,1)]).circle(15,mode='s').finalize().extrude(-20)).union(w0.workplane(offset=40/2).cylinder(40,15))
