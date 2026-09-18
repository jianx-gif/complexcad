import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-100,0))
w1=cq.Workplane('ZX',origin=(0,-38,0))
r=w0.sketch().segment((-57,53),(-57,54)).segment((-56,54)).segment((-56,53)).arc((-56,56),(-57,53)).assemble().finalize().extrude(200).union(w1.workplane(offset=49/2).moveTo(0,1).cylinder(49,4))