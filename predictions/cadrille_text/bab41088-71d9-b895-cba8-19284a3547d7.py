import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-67,-67))
r=w0.sketch().segment((-100,67),(-99,67)).segment((-99,65)).segment((-96,65)).segment((-96,67)).segment((-95,67)).segment((-95,70)).segment((-96,70)).segment((-96,72)).segment((-99,72)).segment((-99,70)).segment((-100,70)).close().assemble().finalize().extrude(133)