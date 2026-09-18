import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-95))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().circle(48).circle(46,mode='s').finalize().extrude(22).union(w0.workplane(offset=130/2).cylinder(130,41)).union(w1.sketch().arc((28,10),(-29,-12),(29,7)).arc((24,8),(28,10)).assemble().finalize().extrude(200))