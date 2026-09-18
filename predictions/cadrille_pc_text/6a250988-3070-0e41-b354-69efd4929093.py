import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,63))
w1=cq.Workplane('YZ',origin=(25,0,0))
r=w0.sketch().circle(100).circle(40,mode='s').finalize().extrude(-143).union(w0.sketch().circle(73).circle(39,mode='s').finalize().extrude(10)).union(w1.sketch().arc((-72,68),(67,-59),(-63,73)).segment((-63,68)).close().assemble().finalize().extrude(-106))