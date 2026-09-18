import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-47))
w1=cq.Workplane('XY',origin=(0,0,-19))
r=w0.sketch().segment((-94,-38),(-85,-38)).segment((-85,-55)).arc((89,43),(-94,-38)).assemble().circle(82,mode='s').finalize().extrude(94).union(w1.sketch().circle(100).circle(94,mode='s').finalize().extrude(32))