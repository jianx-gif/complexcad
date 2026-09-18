import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-22))
r=w0.sketch().rect(200,150).push([(52,56)]).circle(10,mode='s').finalize().extrude(15).union(w0.sketch().segment((-38,-74),(37,-74)).segment((37,74)).segment((-36,75)).close().assemble().circle(13,mode='s').finalize().extrude(45))