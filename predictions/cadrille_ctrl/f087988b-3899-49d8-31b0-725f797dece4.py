import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,10))
r=w0.sketch().arc((-40,0),(40,-3),(-39,7)).arc((-37,3),(-40,0)).assemble().finalize().extrude(-10).union(w0.sketch().circle(15).circle(14,mode='s').finalize().extrude(8))
