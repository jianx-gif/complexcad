import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,20))
r=w0.workplane(offset=-41/2).moveTo(0,-0.5).box(20,55,41).union(w0.sketch().segment((-40,-30),(40,-30)).segment((40,30)).segment((-38,30)).arc((-39,28),(-40,27)).close().assemble().push([(-30,19)]).circle(2,mode='s').push([(28,-19)]).circle(2,mode='s').push([(28,19)]).circle(2).finalize().extrude(-20))