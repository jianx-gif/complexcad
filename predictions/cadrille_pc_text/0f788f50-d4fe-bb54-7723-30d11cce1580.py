import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-5))
r=w0.sketch().segment((-75,35),(75,35)).segment((75,50)).segment((59,50)).segment((59,37)).segment((33,37)).segment((33,50)).segment((-75,50)).close().assemble().finalize().extrude(-10).union(w0.sketch().rect(200,150).rect(100,76,mode='s').finalize().extrude(20))