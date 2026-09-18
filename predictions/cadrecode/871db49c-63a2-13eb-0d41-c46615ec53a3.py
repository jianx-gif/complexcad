import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,23))
r=w0.sketch().segment((-22,-3),(-17,-3)).arc((18,1),(-17,3)).segment((-21,3)).arc((22,-2),(-22,-3)).assemble().finalize().extrude(-123).union(w0.sketch().circle(26).circle(23,mode='s').finalize().extrude(-88)).union(w0.sketch().circle(15).circle(11,mode='s').finalize().extrude(77))