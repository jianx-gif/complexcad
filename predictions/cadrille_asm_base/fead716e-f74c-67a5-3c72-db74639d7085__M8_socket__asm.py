import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-35))
w1=cq.Workplane('XY',origin=(0,0,-17))
r=w0.sketch().circle(17).circle(11,mode='s').finalize().extrude(70).union(w1.sketch().segment((-100,-100),(100,-100)).segment((100,100)).segment((-100,100)).segment((-100,57)).arc((-97,56),(-100,55)).close().assemble().push([(-50,53)]).circle(8,mode='s').push([(51,52)]).circle(8,mode='s').finalize().extrude(20))