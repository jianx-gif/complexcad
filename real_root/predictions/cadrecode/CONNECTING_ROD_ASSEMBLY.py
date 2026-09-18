import cadquery as cq
w0=cq.Workplane('YZ',origin=(-42,0,0))
w1=cq.Workplane('ZX',origin=(0,-19,0))
r=w0.workplane(offset=-58/2).cylinder(58,10).union(w0.sketch().segment((-6,-10),(-3,-10)).segment((-3,-12)).segment((6,-12)).segment((6,-9)).segment((2,-9)).segment((2,-2)).segment((6,-2)).segment((6,9)).segment((-6,9)).close().assemble().finalize().extrude(135)).union(w0.sketch().circle(12).circle(10,mode='s').finalize().extrude(142)).union(w1.sketch().push([(0,-59)]).circle(28).circle(22,mode='s').finalize().extrude(38))