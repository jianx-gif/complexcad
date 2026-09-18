import cadquery as cq
w0=cq.Workplane('YZ',origin=(-100,0,0))
r=w0.sketch().segment((-30,-17),(30,-17)).segment((30,-1)).segment((12,-1)).segment((12,5)).segment((-12,5)).segment((-12,-1)).segment((-30,-1)).close().assemble().push([(-4,-5)]).circle(3,mode='s').finalize().extrude(200)