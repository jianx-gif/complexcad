import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,83))
r=w0.sketch().segment((37,-85),(37,51)).segment((64,51)).segment((64,-77)).arc((-55,83),(49,-88)).segment((49,-85)).close().assemble().circle(8,mode='s').finalize().extrude(-166).union(w0.sketch().circle(98).push([(33,14)]).circle(35,mode='s').finalize().extrude(-146))