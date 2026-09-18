import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-2))
r=w0.sketch().segment((-100,-49),(-65,-49)).segment((-62,-52)).segment((-59,-49)).segment((100,-49)).segment((100,51)).segment((-100,51)).close().assemble().push([(53,-13)]).circle(3,mode='s').finalize().extrude(5)