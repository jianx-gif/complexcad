import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
w1=cq.Workplane('YZ',origin=(33,0,0))
r=w0.sketch().segment((40,-12),(47,-12)).segment((47,15)).segment((40,15)).arc((41,1),(40,-12)).assemble().finalize().extrude(-7).union(w0.sketch().circle(40).circle(35,mode='s').finalize().extrude(80)).union(w1.workplane(offset=-133/2).moveTo(-4,0).cylinder(133,1))
