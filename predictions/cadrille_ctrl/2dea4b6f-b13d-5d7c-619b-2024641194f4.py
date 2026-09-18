import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,10))
r=w0.sketch().segment((-40,-10),(-39,-10)).segment((-39,-11)).arc((-29,-27),(-12,-37)).segment((-12,-39)).segment((-10,-39)).segment((-10,-38)).arc((39,10),(-29,20)).segment((-39,20)).arc((40,-1),(-40,-10)).assemble().push([(33,-1)]).circle(2,mode='s').finalize().extrude(-10).union(w0.sketch().segment((-32,19),(-29,19)).segment((-29,21)).segment((-32,21)).arc((-31,20),(-32,19)).assemble().finalize().extrude(-10))
