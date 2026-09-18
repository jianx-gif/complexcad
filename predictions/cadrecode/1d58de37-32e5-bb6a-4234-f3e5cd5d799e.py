import cadquery as cq
w0=cq.Workplane('YZ',origin=(80,0,0))
w1=cq.Workplane('YZ',origin=(78,0,0))
r=w0.sketch().segment((-60,-6),(42,-6)).segment((42,6)).segment((-59,6)).segment((-59,0)).segment((-60,0)).close().assemble().finalize().extrude(-180).union(w0.workplane(offset=20/2).moveTo(29,0).cylinder(20,31)).union(w1.sketch().push([(-9,0)]).rect(102,12).push([(29,0)]).circle(4,mode='s').finalize().extrude(-156))