import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,5))
r=w0.sketch().segment((-40,-30),(40,-30)).segment((40,30)).segment((-40,30)).segment((-40,25)).arc((-38,24),(-40,23)).close().assemble().circle(19,mode='s').finalize().extrude(-5).union(w0.sketch().rect(80,60).circle(21,mode='s').finalize().extrude(-5))
