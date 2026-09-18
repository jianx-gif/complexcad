import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,32))
w1=cq.Workplane('ZX',origin=(0,-27,0))
r=w0.sketch().circle(58).circle(53,mode='s').finalize().extrude(-128).union(w0.workplane(offset=-123/2).cylinder(123,53)).union(w0.sketch().segment((-69,10),(-68,10)).arc((0,-65),(68,10)).segment((69,10)).segment((69,12)).segment((68,12)).arc((0,67),(-68,12)).segment((-69,12)).close().assemble().finalize().extrude(40)).union(w1.sketch().push([(44,0)]).circle(56).circle(54,mode='s').finalize().extrude(91))