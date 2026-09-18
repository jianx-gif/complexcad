import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,0,0))
w1=cq.Workplane('ZX',origin=(0,0,0))
r=w0.sketch().segment((0,8),(6,8)).segment((6,24)).segment((0,24)).segment((0,23)).arc((2,22),(0,21)).close().assemble().finalize().extrude(-10).union(w0.sketch().push([(0,0)]).circle(30).circle(28,mode='s').finalize().extrude(45)).union(w1.sketch().arc((1,-29),(30,0),(1,29)).close().assemble().finalize().extrude(45))
