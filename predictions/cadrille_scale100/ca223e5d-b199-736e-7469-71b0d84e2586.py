import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,70))
r=w0.sketch().segment((-30,2),(-29,2)).arc((-28,1),(-28,0)).segment((-28,-1)).segment((-29,-1)).arc((-29,-2),(-30,-2)).arc((-27,-1),(-25,-1)).arc((27,7),(-25,13)).arc((-27,13),(-29,12)).segment((-30,12)).arc((30,1),(-30,2)).assemble().finalize().extrude(-70).union(w0.workplane(offset=-29/2).cylinder(29,35))