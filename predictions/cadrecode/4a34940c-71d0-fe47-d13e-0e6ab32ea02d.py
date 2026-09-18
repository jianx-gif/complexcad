import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,68))
r=w0.sketch().arc((85,-1),(86,0),(85,1)).close().assemble().finalize().extrude(-136).union(w0.sketch().circle(100).circle(83,mode='s').finalize().extrude(-133))