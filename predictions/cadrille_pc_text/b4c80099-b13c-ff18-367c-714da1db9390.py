import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,6))
w1=cq.Workplane('XY',origin=(0,0,18))
r=w0.sketch().segment((-98,-26),(-95,-26)).arc((0,-100),(95,-26)).segment((98,-26)).segment((98,26)).segment((95,26)).arc((0,100),(-95,26)).segment((-98,26)).close().assemble().circle(93,mode='s').finalize().extrude(-33).union(w1.sketch().circle(93).circle(72,mode='s').finalize().extrude(10))