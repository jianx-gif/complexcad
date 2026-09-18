import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-25))
w1=cq.Workplane('YZ',origin=(-53,0,0))
r=w0.sketch().circle(75).circle(53,mode='s').finalize().extrude(-24).union(w0.workplane(offset=125/2).moveTo(-1,0).cylinder(125,50)).union(w1.sketch().push([(0,-61)]).circle(39).circle(21,mode='s').finalize().extrude(96))