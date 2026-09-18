import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-56))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().segment((24,-58),(29,-58)).segment((29,-55)).arc((27,-56),(24,-58)).assemble().finalize().extrude(156).union(w1.workplane(offset=100/2).moveTo(0,1).cylinder(100,3))