import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,22))
r=w0.sketch().circle(100).reset().face(w0.sketch().segment((-90,-1),(-28,-15)).arc((-10,-32),(14,-27)).segment((86,-41)).segment((90,-1)).segment((28,15)).arc((10,32),(-14,27)).segment((-86,41)).close().assemble(),mode='s').finalize().extrude(-44).union(w0.sketch().circle(83).circle(43,mode='s').finalize().extrude(-6))