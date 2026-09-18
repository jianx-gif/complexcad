import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,38))
r=w0.sketch().segment((-100,-41),(-97,-41)).segment((-97,-50)).segment((100,-50)).segment((100,50)).segment((-97,50)).segment((-97,49)).segment((-100,49)).segment((-100,32)).arc((-94,26),(-100,20)).close().assemble().push([(-62,25)]).circle(6,mode='s').finalize().extrude(-76)