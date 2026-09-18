import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,37))
r=w0.sketch().segment((-100,-47),(-97,-47)).segment((-97,-50)).segment((100,-50)).segment((100,50)).segment((-97,50)).segment((-97,47)).segment((-100,47)).close().assemble().push([(-96,21)]).circle(3,mode='s').push([(-63,25)]).circle(6,mode='s').finalize().extrude(-75)