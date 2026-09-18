import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-63,0))
w1=cq.Workplane('XY',origin=(0,0,25))
r=w0.workplane(offset=126/2).moveTo(12,0).cylinder(126,5).union(w1.sketch().segment((-100,-39),(-97,-39)).segment((-97,-50)).segment((95,-50)).segment((95,-39)).segment((100,-39)).segment((100,39)).segment((95,39)).segment((95,50)).segment((-97,50)).segment((-97,39)).segment((-100,39)).close().assemble().rect(190,90,mode='s').finalize().extrude(-50))