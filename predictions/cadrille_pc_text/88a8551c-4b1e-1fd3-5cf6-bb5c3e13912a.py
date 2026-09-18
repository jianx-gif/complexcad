import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,2))
r=w0.sketch().segment((-100,-100),(100,-100)).segment((100,60)).segment((30,60)).segment((30,100)).segment((-30,100)).segment((-30,60)).segment((-100,60)).close().assemble().push([(-53,-23)]).circle(40,mode='s').push([(0,-80)]).rect(180,20,mode='s').finalize().extrude(-16).union(w0.workplane(offset=12/2).moveTo(0,-20).box(182,20,12))