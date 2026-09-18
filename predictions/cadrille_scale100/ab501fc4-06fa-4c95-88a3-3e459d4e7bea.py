import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,2))
w1=cq.Workplane('ZX',origin=(0,0,0))
r=w0.sketch().segment((-29,-16),(-17,-27)).segment((-17,-30)).segment((-13,-30)).segment((-10,-32)).segment((-8,-30)).segment((17,-30)).segment((17,-16)).arc((28,15),(-3,31)).segment((-5,32)).segment((-7,30)).segment((-17,30)).segment((-17,16)).arc((-28,-3),(-25,-24)).close().assemble().finalize().extrude(-2).union(w0.workplane(offset=18/2).moveTo(0,0).cylinder(18,10)).union(w1.sketch().push([(0,0)]).circle(40).circle(30,mode='s').finalize().extrude(8))