import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,5))
r=w0.sketch().segment((-100,-60),(60,-60)).segment((60,-10)).segment((100,-10)).segment((100,10)).segment((60,10)).segment((60,60)).segment((-100,60)).close().assemble().push([(36,-44)]).circle(4,mode='s').finalize().extrude(-10)