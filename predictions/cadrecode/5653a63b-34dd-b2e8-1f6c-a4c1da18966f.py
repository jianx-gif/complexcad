import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-72,0))
r=w0.sketch().segment((-72,-49),(-50,-49)).segment((-50,-85)).segment((50,-85)).segment((50,85)).segment((-50,85)).segment((-50,49)).segment((-72,49)).close().assemble().circle(27,mode='s').finalize().extrude(55).union(w0.sketch().circle(100).circle(45,mode='s').push([(61,11.5)]).rect(22,133,mode='s').finalize().extrude(144))