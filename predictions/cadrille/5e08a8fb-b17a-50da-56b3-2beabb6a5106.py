import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-37))
r=w0.sketch().segment((-100,-62),(96,-63)).segment((96,-57)).segment((100,-57)).segment((100,57)).segment((96,57)).segment((96,62)).segment((-96,63)).segment((-96,57)).segment((-100,57)).close().assemble().circle(10,mode='s').finalize().extrude(75)