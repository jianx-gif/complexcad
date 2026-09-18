import cadquery as cq
w0=cq.Workplane('YZ',origin=(-100,0,0))
r=w0.sketch().segment((-38,-31),(37,-31)).arc((31,-9),(14,6)).segment((20,31)).segment((-19,31)).segment((-23,16)).segment((-30,16)).segment((-30,-6)).close().assemble().push([(4,0)]).circle(24,mode='s').finalize().extrude(200)