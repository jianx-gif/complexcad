import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,2))
r=w0.sketch().segment((-100,-49),(-25,-49)).arc((0,-54),(25,-49)).segment((100,-49)).segment((100,51)).segment((25,51)).arc((0,56),(-25,51)).segment((-100,51)).close().assemble().push([(34,10)]).circle(10,mode='s').finalize().extrude(-5)