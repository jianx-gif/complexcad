import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-29))
w1=cq.Workplane('YZ',origin=(-29,0,0))
r=w0.sketch().segment((-39,-1),(-13,-22)).segment((39,0)).segment((37,1)).arc((28,1),(21,5)).segment((13,5)).arc((0,0),(-13,0)).segment((-34,0)).segment((-34,1)).close().assemble().finalize().extrude(58).union(w1.workplane(offset=108/2).moveTo(0,-1).cylinder(108,1))