import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-50))
r=w0.sketch().circle(100).reset().face(w0.sketch().segment((-23,-16),(1,-25)).segment((1,-29)).segment((11,-29)).segment((54,-44)).segment((80,26)).segment((56,35)).segment((56,39)).segment((46,39)).segment((2,54)).close().assemble(),mode='s').finalize().extrude(60).union(w0.workplane(offset=100/2).cylinder(100,60))