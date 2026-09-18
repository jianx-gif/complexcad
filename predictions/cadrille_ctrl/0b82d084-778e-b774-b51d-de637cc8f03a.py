import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,6))
w1=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().arc((-49,-14),(-43,-15),(-48,-17)).arc((49,10),(-49,-14)).assemble().push([(0,-3)]).circle(32,mode='s').finalize().extrude(-5).union(w0.sketch().push([(0,-3)]).circle(40).circle(38,mode='s').finalize().extrude(14)).union(w1.sketch().push([(0,-3)]).circle(47).circle(31,mode='s').finalize().extrude(-1))
