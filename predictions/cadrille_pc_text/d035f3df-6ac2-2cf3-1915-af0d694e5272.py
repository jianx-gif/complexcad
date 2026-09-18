import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-62,35),(-58,-37)).segment((62,-36)).segment((58,38)).close().assemble().push([(-25,-1)]).circle(5,mode='s').push([(25,-1)]).circle(5,mode='s').finalize().extrude(-200).union(w0.workplane(offset=-188/2).cylinder(188,53))