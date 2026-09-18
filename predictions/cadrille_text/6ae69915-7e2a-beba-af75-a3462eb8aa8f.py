import cadquery as cq
w0=cq.Workplane('XY',origin=(-67,-19,-100))
r=w0.sketch().segment((24,-58),(24,-57)).segment((26,-57)).arc((28,-56),(30,-57)).segment((32,-57)).arc((28,-54),(24,-58)).assemble().finalize().extrude(200)