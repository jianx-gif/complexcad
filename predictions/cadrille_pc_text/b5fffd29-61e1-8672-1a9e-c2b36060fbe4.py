import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,12))
r=w0.sketch().segment((-100,-75),(100,-75)).segment((100,75)).segment((-100,75)).segment((-100,24)).arc((-97,22),(-100,20)).close().assemble().circle(40,mode='s').finalize().extrude(-24)