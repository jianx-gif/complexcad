import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,45))
w1=cq.Workplane('XY',origin=(0,0,80))
r=w0.sketch().segment((-20,5),(-10,-20)).segment((20,-5)).segment((10,20)).close().assemble().finalize().extrude(15).union(w1.workplane(offset=-80/2).cylinder(80,12))