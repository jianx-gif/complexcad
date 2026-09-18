import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,0,-100))
r=w0.sketch().segment((91,-59),(100,-59)).segment((100,-48)).arc((96,-54),(91,-59)).assemble().finalize().extrude(200)