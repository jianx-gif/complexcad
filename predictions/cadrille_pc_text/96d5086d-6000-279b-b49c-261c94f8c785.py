import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,5))
w1=cq.Workplane('XY',origin=(0,0,18))
r=w0.sketch().segment((-100,-22),(78,-22)).segment((78,-11)).segment((100,-11)).segment((100,11)).segment((78,11)).segment((78,22)).segment((-100,22)).close().assemble().push([(-56,0)]).circle(7,mode='s').finalize().extrude(-23).union(w1.sketch().segment((-87,-13),(64,-13)).segment((64,13)).segment((-87,13)).segment((-87,11)).arc((-84,10),(-87,9)).close().assemble().finalize().extrude(-17))