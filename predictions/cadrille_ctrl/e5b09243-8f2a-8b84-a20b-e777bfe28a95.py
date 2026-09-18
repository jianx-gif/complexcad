import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-29))
w1=cq.Workplane('YZ',origin=(-29,0,0))
r=w0.sketch().segment((-39,-1),(-13,-22)).segment((39,0)).segment((37,1)).arc((25,0),(13,6)).arc((-13,0),(-39,-1)).assemble().finalize().extrude(58).union(w1.workplane(offset=58/2).moveTo(-1,0).cylinder(58,2))
