import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-51))
w1=cq.Workplane('XY',origin=(0,0,-26))
r=w0.sketch().segment((-38,11),(-38,24)).arc((-39,18),(-38,11)).assemble().finalize().extrude(-7).union(w1.sketch().segment((-28,-1),(-28,1)).segment((-23,1)).segment((-23,0)).segment((-22,0)).segment((-22,-1)).segment((-23,-1)).segment((-23,-2)).segment((-24,-2)).arc((-25,0),(-28,-1)).assemble().finalize().extrude(126))