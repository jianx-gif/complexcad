import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().segment((-12,10),(-11,10)).segment((-11,11)).segment((-12,11)).close().assemble().finalize().extrude(-1).union(w0.sketch().segment((-10,-10),(1,-15)).segment((15,7)).segment((13,9)).segment((12,9)).segment((12,10)).segment((-1,16)).close().assemble().finalize().extrude(3)).union(w0.sketch().segment((-9,5),(-7,5)).segment((-7,7)).segment((-9,7)).segment((-9,6)).close().assemble().finalize().extrude(3))
