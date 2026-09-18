import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,5))
r=w0.sketch().segment((-100,-32),(-96,-32)).segment((-96,-50)).segment((93,-47)).segment((92,-32)).segment((100,-32)).segment((100,32)).segment((92,32)).segment((92,50)).segment((-93,48)).segment((-93,32)).segment((-100,32)).close().assemble().push([(-37,4)]).circle(7,mode='s').finalize().extrude(-10)