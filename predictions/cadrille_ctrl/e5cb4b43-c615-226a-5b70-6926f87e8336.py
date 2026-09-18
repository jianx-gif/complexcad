import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-2))
r=w0.sketch().rect(80,80).circle(32,mode='s').finalize().extrude(-1).union(w0.sketch().segment((-34,-11),(-14,-11)).segment((-14,-33)).segment((14,-33)).segment((14,-11)).segment((34,-11)).segment((34,11)).segment((14,11)).segment((14,33)).segment((-14,33)).segment((-14,11)).segment((-34,11)).close().assemble().finalize().extrude(7)).union(w0.workplane(offset=22/2).cylinder(22,21))
