import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,1))
r=w0.sketch().segment((-100,-75),(100,-75)).segment((100,75)).segment((-100,75)).segment((-100,-38)).segment((-90,-38)).segment((-90,-62)).segment((-100,-62)).close().assemble().finalize().extrude(-10).union(w0.sketch().rect(50,100).push([(14,-4)]).circle(11,mode='s').finalize().extrude(8))