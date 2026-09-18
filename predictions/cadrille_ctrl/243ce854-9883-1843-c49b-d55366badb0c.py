import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().segment((-39,-2),(-20,-2)).arc((-21,0),(-20,2)).segment((-39,2)).close().assemble().finalize().extrude(-80).union(w0.sketch().segment((-39,-2),(-20,-34)).segment((-13,-30)).segment((-13,-34)).segment((21,-34)).segment((21,-13)).segment((39,-2)).segment((21,30)).segment((21,34)).segment((18,34)).segment((17,34)).segment((-13,34)).segment((-13,13)).close().assemble().finalize().extrude(20)).union(w0.workplane(offset=80/2).moveTo(0,0).cylinder(80,32))
