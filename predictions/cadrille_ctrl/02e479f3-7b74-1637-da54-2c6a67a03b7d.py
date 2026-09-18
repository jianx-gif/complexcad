import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,5))
w1=cq.Workplane('XY',origin=(0,0,28))
r=w0.sketch().segment((-39,4),(-35,-1)).arc((-28,-21),(-10,-33)).segment((-6,-39)).segment((0,-35)).arc((21,-31),(35,-15)).segment((39,-12)).segment((35,-6)).arc((28,24),(0,38)).segment((-4,44)).segment((-10,40)).arc((-26,30),(-36,13)).segment((-39,11)).segment((-36,8)).arc((-36,7),(-35,6)).close().assemble().finalize().extrude(4).union(w0.sketch().push([(2,0)]).circle(29).circle(24,mode='s').finalize().extrude(23)).union(w0.sketch().push([(2,0)]).circle(28).circle(21,mode='s').finalize().extrude(29)).union(w1.workplane(offset=-5/2).moveTo(2,0).cylinder(5,21))
