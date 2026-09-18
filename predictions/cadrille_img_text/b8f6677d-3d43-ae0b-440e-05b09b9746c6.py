import cadquery as cq
w0=cq.Workplane('YZ',origin=(100,0,0))
w1=cq.Workplane('ZX',origin=(0,-33,0))
r=w0.sketch().arc((-95,-35),(-89,-36),(-83,-37)).segment((74,35)).segment((-43,37)).arc((-47,36),(-50,37)).close().assemble().reset().face(w0.sketch().arc((83,-37),(95,0),(83,37)).close().assemble()).finalize().extrude(-200).union(w1.sketch().push([(28,43)]).circle(42).circle(33,mode='s').finalize().extrude(-33))