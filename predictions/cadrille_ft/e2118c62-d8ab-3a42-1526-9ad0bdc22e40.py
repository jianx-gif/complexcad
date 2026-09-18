import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,83))
r=w0.sketch().segment((37,-85),(37,51)).segment((64,51)).segment((64,77)).arc((-100,0),(64,-77)).segment((64,-85)).close().assemble().circle(8,mode='s').finalize().extrude(-166).union(w0.sketch().circle(90).push([(45,14)]).circle(24,mode='s').finalize().extrude(-146))