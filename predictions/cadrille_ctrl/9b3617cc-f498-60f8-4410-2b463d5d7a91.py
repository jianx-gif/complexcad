import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.workplane(offset=-55/2).moveTo(-2,0).cylinder(55,2).union(w0.sketch().arc((-27,11),(-29,-6),(-21,-21)).segment((-21,-1)).segment((3,-1)).segment((3,-29)).segment((-5,-29)).arc((28,-11),(13,25)).arc((-10,28),(-27,11)).assemble().push([(2,25)]).circle(1,mode='s').finalize().extrude(13)).union(w0.sketch().push([(0,-1)]).circle(17).circle(3,mode='s').finalize().extrude(55))
