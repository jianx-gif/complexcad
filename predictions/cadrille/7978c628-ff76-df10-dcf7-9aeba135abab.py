import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,7))
w1=cq.Workplane('YZ',origin=(-50,0,0))
r=w0.sketch().segment((-100,-13),(-96,-13)).segment((-96,-18)).segment((-78,-18)).arc((-70,3),(-71,23)).segment((-96,22)).segment((-96,23)).segment((-100,23)).close().assemble().reset().face(w0.sketch().segment((-66,-18),(96,-18)).segment((96,-13)).segment((100,-13)).segment((100,23)).segment((96,23)).segment((96,22)).segment((70,22)).segment((70,-3)).segment((-66,-3)).close().assemble()).finalize().extrude(-20).union(w1.workplane(offset=98/2).moveTo(-21,7).box(4,14,98))