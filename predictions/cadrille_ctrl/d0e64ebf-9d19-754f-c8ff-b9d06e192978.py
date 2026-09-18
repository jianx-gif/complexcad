import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,60))
r=w0.sketch().arc((12,38),(13,37),(14,37)).arc((13,38),(12,38)).assemble().finalize().extrude(-120).union(w0.sketch().circle(40).circle(15,mode='s').finalize().extrude(-60))
