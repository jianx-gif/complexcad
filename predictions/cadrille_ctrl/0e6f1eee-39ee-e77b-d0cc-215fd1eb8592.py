import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.workplane(offset=-12/2).moveTo(-38,-29).cylinder(12,2).union(w0.workplane(offset=8/2).moveTo(0,0.5).box(80,59,8)).union(w0.sketch().segment((-40,-30),(40,-30)).segment((40,30)).segment((-40,30)).segment((-40,20)).arc((-32,19),(-25,16)).segment((-25,21)).segment((25,21)).segment((25,-21)).segment((-25,-21)).segment((-25,-10)).arc((-32,-13),(-40,-14)).close().assemble().finalize().extrude(12))
