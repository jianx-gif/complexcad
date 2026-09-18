import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,8))
r=w0.sketch().segment((-30,-15),(-24,-21)).segment((-19,-17)).segment((-26,-17)).segment((-26,-11)).arc((-27,-10),(-27,-8)).close().assemble().finalize().extrude(-10).union(w0.sketch().segment((-24,17),(-23,17)).segment((-23,20)).close().assemble().reset().face(w0.sketch().segment((13,-19),(14,-20)).segment((30,-20)).segment((30,20)).segment((13,20)).close().assemble()).finalize().extrude(-8)).union(w0.sketch().segment((-30,-15),(-24,-20)).segment((-19,-15)).close().assemble().finalize().extrude(-8))
