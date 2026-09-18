import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,1))
r=w0.workplane(offset=-12/2).moveTo(0,-5.5).box(200,67,12).union(w0.sketch().segment((-2,28),(0,28)).segment((0,27)).arc((1,39),(-2,28)).assemble().finalize().extrude(9))