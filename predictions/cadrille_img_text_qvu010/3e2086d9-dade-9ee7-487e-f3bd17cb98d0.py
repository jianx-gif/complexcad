import cadquery as cq
w0=cq.Workplane('YZ',origin=(30,0,0))
w1=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().push([(-1,0)]).circle(99).circle(98,mode='s').finalize().extrude(-129).union(w1.sketch().arc((-58,-72),(-45,-67),(-37,-56)).arc((-35,-54),(-33,-51)).arc((-31,-49),(-29,-47)).arc((-1,29),(20,-49)).arc((22,-51),(24,-53)).arc((30,-57),(35,-63)).arc((47,-70),(58,-79)).arc((-1,85),(-58,-72)).assemble().finalize().extrude(-157))