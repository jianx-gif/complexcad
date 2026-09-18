import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-22))
w1=cq.Workplane('XY',origin=(0,0,-22))
r=w0.sketch().segment((-37,-75),(38,-75)).segment((38,60)).segment((29,60)).segment((29,75)).segment((-37,75)).close().assemble().push([(0,-1)]).circle(13,mode='s').finalize().extrude(45).union(w1.workplane(offset=14/2).box(200,150,14))