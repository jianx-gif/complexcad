import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-10))
r=w0.sketch().segment((-100,-25),(86,-25)).segment((86,-20)).arc((100,0),(86,22)).segment((86,25)).segment((-100,25)).close().assemble().push([(-89,12)]).circle(7,mode='s').push([(0,0)]).rect(190,40,mode='s').finalize().extrude(20)