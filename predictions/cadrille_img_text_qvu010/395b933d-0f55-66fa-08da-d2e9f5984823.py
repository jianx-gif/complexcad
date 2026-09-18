import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,52,0))
w1=cq.Workplane('YZ',origin=(47,0,0))
r=w0.sketch().circle(100).circle(99,mode='s').finalize().extrude(-122).union(w0.sketch().arc((59,-66),(96,0),(59,66)).close().assemble().finalize().extrude(48)).union(w1.sketch().arc((44,-96),(48,-76),(44,-56)).close().assemble().finalize().extrude(-135))