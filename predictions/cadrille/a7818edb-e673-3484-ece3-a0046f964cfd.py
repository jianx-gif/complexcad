import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,15))
r=w0.sketch().segment((-88,82),(-87,82)).segment((-87,-100)).segment((-73,-100)).segment((-73,-85)).segment((87,-85)).segment((87,-82)).segment((88,-82)).segment((87,-82)).segment((87,100)).segment((-87,100)).segment((-87,82)).close().assemble().rect(134,170,mode='s').push([(83,-3)]).circle(2,mode='s').finalize().extrude(-30)