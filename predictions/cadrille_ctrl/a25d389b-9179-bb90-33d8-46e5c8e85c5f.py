import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().arc((22,-33),(23,-31),(25,-31)).arc((-23,33),(22,-33)).assemble().circle(35,mode='s').finalize().extrude(70).union(w0.workplane(offset=70/2).cylinder(70,40))
