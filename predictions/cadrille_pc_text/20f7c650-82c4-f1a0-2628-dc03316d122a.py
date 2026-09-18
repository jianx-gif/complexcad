import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,6))
r=w0.sketch().segment((-35,-97),(-26,-97)).segment((-26,-100)).segment((35,-100)).segment((35,-97)).segment((35,88)).segment((35,92)).segment((26,92)).segment((26,97)).segment((-35,97)).close().assemble().push([(-1,-46)]).circle(4,mode='s').push([(0,0)]).circle(2,mode='s').finalize().extrude(-12)