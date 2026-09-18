import cadquery as cq
w0=cq.Workplane('YZ',origin=(-76,0,0))
w1=cq.Workplane('YZ',origin=(-72,0,0))
r=w0.sketch().segment((-76,-100),(76,-100)).segment((76,90)).segment((10,90)).segment((10,100)).segment((-10,100)).segment((-10,90)).segment((-76,90)).close().assemble().push([(0,-3.5)]).rect(146,185,mode='s').finalize().extrude(152).union(w1.workplane(offset=144/2).moveTo(0,-4.5).box(144,183,144))