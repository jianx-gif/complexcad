import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,65))
w1=cq.Workplane('XY',origin=(0,0,5))
r=w0.sketch().segment((4,-40),(4,40)).arc((-21,0),(4,-40)).assemble().finalize().extrude(-67).union(w0.sketch().arc((-85,-11),(-77,-26),(-77,-43)).arc((82,22),(-85,-11)).assemble().circle(8,mode='s').finalize().extrude(-60)).union(w1.workplane(offset=-65/2).moveTo(0,-1).cylinder(65,3))
