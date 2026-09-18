import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().circle(55).push([(21,-11)]).circle(3,mode='s').finalize().extrude(-16).union(w0.sketch().circle(100).circle(25,mode='s').finalize().extrude(16))