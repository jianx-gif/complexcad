import cadquery as cq
w0=cq.Workplane('YZ',origin=(-95,0,0))
w1=cq.Workplane('YZ',origin=(-100,0,0))
r=w0.workplane(offset=190/2).moveTo(0,-7.5).box(140,5,190).union(w1.sketch().segment((-75,-10),(75,-10)).segment((75,10)).segment((70,10)).segment((70,-6)).segment((-70,-6)).segment((-70,10)).segment((-75,10)).close().assemble().finalize().extrude(200))