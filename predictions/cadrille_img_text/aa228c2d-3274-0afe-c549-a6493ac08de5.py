import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
w1=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().segment((-89,2),(-48,2)).arc((-69,22),(-89,43)).close().assemble().finalize().extrude(-174).union(w1.sketch().arc((-81,-20),(-67,-16),(-54,-12)).arc((-46,38),(-11,82)).segment((-81,82)).close().assemble().finalize().extrude(-182))