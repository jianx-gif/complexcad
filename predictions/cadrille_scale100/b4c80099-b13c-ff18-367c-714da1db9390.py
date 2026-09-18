import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,12))
w1=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().circle(43).circle(31,mode='s').finalize().extrude(-14).union(w0.sketch().circle(40).circle(31,mode='s').finalize().extrude(10)).union(w1.sketch().circle(42).reset().face(w1.sketch().segment((-28,-16),(-24,-16)).arc((0,-31),(24,-16)).segment((28,-16)).segment((28,16)).segment((24,16)).arc((0,31),(-24,16)).segment((-28,16)).close().assemble(),mode='s').finalize().extrude(18))