import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-26))
r=w0.workplane(offset=10/2).moveTo(-68,-24).box(64,26,10).union(w0.sketch().segment((-79,-13),(-34,-8)).arc((18,6),(72,-31)).segment((100,-17)).arc((10,37),(-79,-13)).assemble().finalize().extrude(52))