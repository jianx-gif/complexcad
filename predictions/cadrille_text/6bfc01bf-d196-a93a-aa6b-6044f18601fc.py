import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-66,-32))
r=w0.sketch().segment((96,-49),(100,-49)).segment((100,-47)).arc((98,-48),(96,-49)).assemble().finalize().extrude(65)