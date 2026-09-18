import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,35))
r=w0.sketch().circle(83).circle(12,mode='s').finalize().extrude(-71).union(w0.sketch().circle(82).circle(12,mode='s').finalize().extrude(-71)).union(w0.sketch().circle(100).circle(13,mode='s').finalize().extrude(-7))