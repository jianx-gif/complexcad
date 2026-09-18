import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,75))
r=w0.sketch().push([(0,7)]).circle(23).circle(7,mode='s').finalize().extrude(-175).union(w0.sketch().segment((-49,-10),(49,-12)).segment((49,25)).segment((-49,26)).close().assemble().push([(-37,10)]).circle(4,mode='s').push([(0,7)]).circle(10,mode='s').finalize().extrude(25))