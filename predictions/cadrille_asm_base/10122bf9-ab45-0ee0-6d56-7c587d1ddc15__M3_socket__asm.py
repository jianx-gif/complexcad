import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-21))
w1=cq.Workplane('YZ',origin=(-76,0,0))
r=w0.sketch().segment((-100,-50),(100,-50)).segment((100,48)).arc((93,48),(87,50)).segment((-100,50)).close().assemble().push([(69,20)]).circle(13,mode='s').finalize().extrude(17).union(w0.workplane(offset=57/2).moveTo(0,33).box(134,34,57)).union(w1.sketch().arc((1,-36),(19,0),(1,36)).close().assemble().finalize().extrude(85))