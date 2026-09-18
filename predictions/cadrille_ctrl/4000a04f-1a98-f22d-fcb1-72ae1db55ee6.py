import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.workplane(offset=-50/2).moveTo(0,1).cylinder(50,11).union(w0.sketch().arc((-30,7),(29,-8),(-27,13)).arc((-29,10),(-30,7)).assemble().push([(-1,1)]).circle(24,mode='s').finalize().extrude(38)).union(w0.sketch().push([(0,1)]).circle(20).circle(8,mode='s').finalize().extrude(50))
