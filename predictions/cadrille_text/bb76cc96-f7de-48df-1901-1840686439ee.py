import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,10))
r=w0.sketch().segment((-58,10),(-58,11)).segment((-57,11)).segment((-57,9)).arc((-53,18),(-58,10)).assemble().finalize().extrude(-39).union(w0.sketch().segment((28,-100),(58,-100)).segment((58,-98)).arc((43,-99),(28,-98)).close().assemble().finalize().extrude(2)).union(w0.workplane(offset=28/2).moveTo(0,98).cylinder(28,2))