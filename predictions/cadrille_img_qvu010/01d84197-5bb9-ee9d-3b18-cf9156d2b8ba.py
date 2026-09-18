import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-44,0))
w1=cq.Workplane('ZX',origin=(0,39,0))
r=w0.sketch().circle(100).circle(54,mode='s').finalize().extrude(8).union(w0.sketch().segment((-39,-69),(-39,-39)).arc((0,-54),(39,-39)).segment((39,-69)).arc((74,-1),(39,69)).segment((39,39)).arc((0,54),(-39,39)).segment((-39,69)).arc((-74,-1),(-39,-69)).assemble().finalize().extrude(132)).union(w1.sketch().circle(100).circle(53,mode='s').finalize().extrude(-85))