import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-51))
r=w0.sketch().segment((29,-57),(32,-57)).segment((32,-55)).arc((30,-56),(29,-57)).assemble().finalize().extrude(-49).union(w0.sketch().push([(30,-10)]).circle(2).push([(30.5,-10)]).rect(3,2,mode='s').finalize().extrude(101)).union(w0.workplane(offset=101/2).moveTo(30,-10).cylinder(101,2))