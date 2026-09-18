import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-6))
r=w0.workplane(offset=-48/2).moveTo(43.5,0).box(113,4,48).union(w0.sketch().segment((-100,-60),(93,-60)).segment((93,60)).segment((-48,60)).segment((-48,59)).segment((-51,59)).segment((-51,60)).segment((-100,60)).close().assemble().push([(-6,0)]).circle(14,mode='s').finalize().extrude(60))