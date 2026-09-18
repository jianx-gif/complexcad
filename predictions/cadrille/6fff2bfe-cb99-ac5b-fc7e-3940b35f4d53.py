import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,92))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().circle(69).circle(48,mode='s').finalize().extrude(-192).union(w0.sketch().segment((-83,1),(-69,-45)).segment((-52,-39)).segment((-52,-62)).segment((52,-62)).segment((52,-17)).segment((83,-1)).segment((69,45)).segment((52,39)).segment((52,62)).segment((-52,62)).segment((-52,17)).close().assemble().finalize().extrude(-11)).union(w1.sketch().circle(81).circle(72,mode='s').finalize().extrude(-200))