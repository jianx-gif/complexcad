import cadquery as cq
w0=cq.Workplane('YZ',origin=(-5,0,0))
w1=cq.Workplane('YZ',origin=(-8,0,0))
r=w0.workplane(offset=-95/2).moveTo(0,3).box(40,16,95).union(w0.sketch().segment((-14,-13),(14,-13)).segment((14,16)).segment((-14,16)).segment((-14,12)).arc((-12,11),(-14,10)).close().assemble().finalize().extrude(105)).union(w1.sketch().push([(0,-2.5)]).rect(66,27).rect(60,21,mode='s').finalize().extrude(106))