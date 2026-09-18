import cadquery as cq
w0=cq.Workplane('YZ',origin=(-100,0,0))
r=w0.workplane(offset=50/2).moveTo(0,-20).cylinder(50,15).union(w0.sketch().segment((-38,-15),(38,-15)).segment((1,34)).close().assemble().push([(0,-2)]).circle(10,mode='s').finalize().extrude(200))