import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-67,-67))
r=w0.sketch().segment((92,-89),(100,-89)).segment((100,-86)).close().assemble().finalize().extrude(133)