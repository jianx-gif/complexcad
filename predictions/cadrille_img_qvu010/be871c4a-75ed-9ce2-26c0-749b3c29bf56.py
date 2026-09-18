import cadquery as cq
w0=cq.Workplane('YZ',origin=(-83,0,0))
w1=cq.Workplane('XY',origin=(0,0,-68))
r=w0.sketch().arc((-91,-26),(-79,-32),(-66,-37)).arc((-64,-35),(-62,-34)).segment((-62,-32)).segment((-60,-32)).arc((-52,-11),(-40,9)).segment((-91,26)).close().assemble().finalize().extrude(114).union(w0.sketch().segment((33,11),(58,17)).segment((33,17)).close().assemble().finalize().extrude(167)).union(w1.sketch().segment((-100,-24),(-96,-24)).arc((-95,-21),(-94,-24)).segment((100,-24)).segment((100,-17)).segment((-100,-17)).close().assemble().finalize().extrude(168))