import cadquery as cq
w0=cq.Workplane('YZ',origin=(-100,0,0))
r=w0.workplane(offset=50/2).moveTo(0,-20).cylinder(50,14).union(w0.sketch().segment((-38,-15),(16,-15)).segment((-12,5)).segment((1,20)).segment((24,-1)).segment((12,-15)).segment((38,-15)).segment((0,35)).close().assemble().finalize().extrude(200))