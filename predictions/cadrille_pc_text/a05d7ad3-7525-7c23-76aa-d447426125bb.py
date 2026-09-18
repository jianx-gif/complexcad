import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,6))
r=w0.sketch().segment((-100,-15),(-98,-15)).arc((0,-100),(98,-15)).segment((100,-15)).segment((100,15)).segment((98,15)).arc((0,100),(-98,15)).segment((-100,15)).close().assemble().circle(6,mode='s').push([(-42,-67)]).circle(5,mode='s').finalize().extrude(-12)