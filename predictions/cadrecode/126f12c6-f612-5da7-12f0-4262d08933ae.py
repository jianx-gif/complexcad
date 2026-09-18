import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-6))
r=w0.workplane(offset=-48/2).moveTo(43,0).box(114,4,48).union(w0.sketch().segment((-100,-60),(93,-60)).segment((93,-22)).segment((92,-22)).segment((92,-15)).segment((93,-15)).segment((93,60)).segment((-100,60)).close().assemble().push([(-3,0)]).circle(15,mode='s').finalize().extrude(60))