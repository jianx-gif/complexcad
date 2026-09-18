import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-65))
r=w0.sketch().segment((84,-12),(86,-12)).segment((86,-11)).arc((85,-11),(84,-12)).assemble().finalize().extrude(-3).union(w0.sketch().circle(100).circle(83,mode='s').finalize().extrude(133))