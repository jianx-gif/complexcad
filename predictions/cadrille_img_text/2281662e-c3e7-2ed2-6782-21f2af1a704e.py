import cadquery as cq
w0=cq.Workplane('YZ',origin=(-48,0,0))
w1=cq.Workplane('ZX',origin=(0,-28,0))
r=w0.sketch().segment((-58,-44),(-31,-44)).arc((-45,0),(-31,44)).segment((-58,44)).close().assemble().finalize().extrude(133).union(w1.sketch().push([(10,12)]).circle(88).circle(87,mode='s').finalize().extrude(57))