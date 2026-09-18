import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,1))
w1=cq.Workplane('ZX',origin=(0,10,0))
r=w0.sketch().segment((-100,-7),(-36,-7)).segment((-36,-50)).segment((-21,-50)).segment((-21,-7)).segment((100,-7)).segment((100,79)).segment((-100,79)).close().assemble().push([(0,36)]).circle(9,mode='s').finalize().extrude(-14).union(w0.sketch().segment((-57,-79),(0,-79)).segment((0,-41)).arc((-28,-35),(-57,-38)).close().assemble().finalize().extrude(12)).union(w1.sketch().arc((51,-10),(53,0),(51,10)).close().assemble().finalize().extrude(-110))