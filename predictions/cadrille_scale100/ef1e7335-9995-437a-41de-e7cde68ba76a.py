import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.workplane(offset=6/2).box(80,60,6).union(w0.sketch().segment((-15,-29),(15,-30)).segment((15,29)).segment((-15,30)).close().assemble().circle(5,mode='s').finalize().extrude(18))