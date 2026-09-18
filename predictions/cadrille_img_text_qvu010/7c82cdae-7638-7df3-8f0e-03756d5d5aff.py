import cadquery as cq
w0=cq.Workplane('YZ',origin=(-65,0,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().arc((-86,-43),(-73,-3),(-55,35)).segment((-86,35)).close().assemble().reset().face(w0.sketch().arc((29,35),(47,16),(58,-8)).arc((52,18),(29,35)).assemble()).finalize().extrude(162).union(w1.sketch().segment((-97,-10),(11,-10)).arc((-43,19),(-97,10)).close().assemble().finalize().extrude(-200))