import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-26))
w1=cq.Workplane('YZ',origin=(33,0,0))
r=w0.sketch().segment((-62,-33),(53,-37)).segment((58,33)).segment((43,34)).segment((37,55)).segment((-37,68)).segment((-42,40)).segment((-53,41)).close().assemble().finalize().extrude(-74).union(w0.sketch().arc((-47,-43),(-39,-57),(-25,-58)).arc((36,16),(-47,-33)).close().assemble().finalize().extrude(126)).union(w1.sketch().segment((-44,-26),(-10,-26)).segment((-10,-14)).segment((-44,-14)).arc((-38,-20),(-44,-26)).assemble().finalize().extrude(-89))