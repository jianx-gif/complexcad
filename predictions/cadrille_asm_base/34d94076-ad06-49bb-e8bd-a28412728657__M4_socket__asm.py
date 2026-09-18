import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-60,0))
w1=cq.Workplane('XY',origin=(0,0,25))
r=w0.workplane(offset=120/2).moveTo(12,0).cylinder(120,4).union(w1.sketch().segment((-100,-49),(-95,-49)).segment((-95,-52)).segment((95,-52)).segment((95,-49)).segment((100,-49)).segment((100,43)).segment((95,43)).segment((95,48)).segment((-95,48)).segment((-95,43)).segment((-100,43)).close().assemble().rect(190,94,mode='s').finalize().extrude(-50))