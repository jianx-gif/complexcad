import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,38,0))
r=w0.sketch().circle(100).reset().face(w0.sketch().segment((-97,-1),(-80,-1)).arc((0,-82),(80,-1)).segment((97,-1)).segment((97,1)).segment((80,1)).arc((0,82),(-80,1)).segment((-97,1)).close().assemble(),mode='s').finalize().extrude(-76)