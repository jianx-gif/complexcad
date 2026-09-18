import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().segment((28,-58),(28,-57)).segment((30,-57)).arc((29,-56),(28,-58)).assemble().finalize().extrude(200)