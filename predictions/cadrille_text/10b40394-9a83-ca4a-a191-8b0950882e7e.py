import cadquery as cq
w0=cq.Workplane('XY',origin=(-57,0,-100))
r=w0.sketch().segment((28,-58),(57,-58)).segment((57,-10)).arc((43,-35),(28,-58)).assemble().finalize().extrude(200)