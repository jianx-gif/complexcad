import cadquery as cq
w0=cq.Workplane('YZ',origin=(-36,0,0))
w1=cq.Workplane('XY',origin=(0,0,-32))
r=w0.sketch().push([(0,-56)]).circle(25).circle(14,mode='s').finalize().extrude(-24).union(w0.sketch().push([(0,-56)]).circle(33).circle(32,mode='s').finalize().extrude(108)).union(w0.sketch().push([(0,-56)]).circle(26).circle(22,mode='s').finalize().extrude(123)).union(w1.sketch().push([(-61,0)]).circle(24).circle(21,mode='s').finalize().extrude(122))