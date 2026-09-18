import cadquery as cq
w0=cq.Workplane('YZ',origin=(40,0,0))
w1=cq.Workplane('ZX',origin=(0,39,0))
r=w0.sketch().segment((-58,-44),(-58,44)).arc((-74,0),(-58,-44)).assemble().reset().face(w0.sketch().arc((58,-44),(74,0),(58,44)).close().assemble()).finalize().extrude(60).union(w1.sketch().push([(12,14)]).circle(86).circle(77,mode='s').finalize().extrude(-79))