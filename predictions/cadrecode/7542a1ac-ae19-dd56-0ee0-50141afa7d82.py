import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-22,0))
w1=cq.Workplane('XY',origin=(0,0,-53))
r=w0.sketch().segment((-100,13),(-88,7)).arc((-67,-19),(-35,-20)).segment((-23,-26)).segment((-17,-13)).segment((-29,-7)).arc((-50,19),(-82,20)).segment((-93,24)).close().assemble().push([(-58,0)]).circle(29,mode='s').finalize().extrude(44).union(w0.sketch().segment((-90,15),(-43,-30)).segment((-36,-23)).segment((-83,22)).close().assemble().finalize().extrude(54)).union(w1.sketch().push([(-37,0)]).circle(24).circle(23,mode='s').finalize().extrude(124))