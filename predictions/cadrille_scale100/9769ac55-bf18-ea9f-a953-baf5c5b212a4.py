import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,15))
r=w0.sketch().arc((-35,19),(-34,18),(-34,17)).arc((34,-18),(-27,28)).arc((-28,28),(-29,29)).arc((34,-18),(-35,19)).assemble().finalize().extrude(-16).union(w0.sketch().push([(0,0)]).circle(40).circle(12,mode='s').finalize().extrude(-5))