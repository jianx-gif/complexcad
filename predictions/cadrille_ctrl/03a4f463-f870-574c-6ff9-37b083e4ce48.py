import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,4))
r=w0.sketch().segment((-40,-20),(-34,-20)).arc((-37,-13),(-34,-6)).segment((-40,-6)).close().assemble().reset().face(w0.sketch().segment((-31,16),(-24,16)).segment((-24,20)).segment((-29,20)).arc((-29,18),(-31,16)).assemble()).reset().face(w0.sketch().segment((-21,16),(-16,16)).segment((-16,20)).segment((-21,20)).arc((-19,18),(-21,16)).assemble()).push([(17,0)]).rect(46,40).finalize().extrude(-8).union(w0.sketch().segment((-39,-16),(-37,-20)).segment((-19,-12)).segment((-21,-8)).close().assemble().finalize().extrude(-8))
