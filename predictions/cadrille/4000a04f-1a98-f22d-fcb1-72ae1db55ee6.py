import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-83))
w1=cq.Workplane('XY',origin=(0,0,-82))
r=w0.sketch().circle(100).circle(84,mode='s').finalize().extrude(126).union(w0.sketch().circle(67).reset().face(w0.sketch().segment((-36,7),(1,-36)).segment((36,-7)).segment((-1,36)).close().assemble(),mode='s').finalize().extrude(166)).union(w1.sketch().circle(40).circle(31,mode='s').finalize().extrude(92))