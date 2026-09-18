import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-15))
r=w0.sketch().segment((-97,-21),(-91,-21)).segment((-91,-31)).segment((-93,-31)).arc((93,27),(-97,-21)).assemble().push([(-32,60)]).circle(27,mode='s').finalize().extrude(-7).union(w0.sketch().circle(96).circle(92,mode='s').circle(33).circle(11,mode='s').finalize().extrude(37))