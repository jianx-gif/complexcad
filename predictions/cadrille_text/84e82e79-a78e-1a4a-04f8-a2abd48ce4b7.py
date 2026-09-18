import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-47,-47))
r=w0.sketch().segment((96,-47),(100,-47)).segment((100,-42)).arc((98,-44),(96,-47)).assemble().finalize().extrude(94)