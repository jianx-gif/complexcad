import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,60))
r=w0.workplane(offset=-120/2).cylinder(120,15).union(w0.sketch().segment((-22,5),(-17,-16)).segment((22,-5)).segment((17,16)).close().assemble().finalize().extrude(-11)).union(w0.workplane(offset=-8/2).cylinder(8,22))