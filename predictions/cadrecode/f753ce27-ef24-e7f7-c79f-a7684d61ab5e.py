import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,32,0))
w1=cq.Workplane('YZ',origin=(76,0,0))
r=w0.sketch().push([(0,42)]).circle(38).circle(30,mode='s').finalize().extrude(-61).union(w0.sketch().push([(0,42)]).circle(58).circle(38,mode='s').finalize().extrude(-27)).union(w1.workplane(offset=-176/2).moveTo(-29,31).cylinder(176,3))