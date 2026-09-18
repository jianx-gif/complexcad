import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,12))
r=w0.sketch().segment((-40,-29),(40,-30)).segment((40,30)).segment((-40,30)).close().assemble().push([(-31,-24)]).circle(3,mode='s').push([(33.5,-20)]).rect(5,4,mode='s').finalize().extrude(-12).union(w0.sketch().circle(15).push([(2,1)]).circle(4,mode='s').finalize().extrude(20))
