import cadquery as cq
w0=cq.Workplane('YZ',origin=(100,0,0))
w1=cq.Workplane('YZ',origin=(60,0,0))
r=w0.sketch().segment((-25,-4),(25,-4)).arc((22,4),(17,9)).segment((-18,9)).arc((-22,5),(-25,-1)).close().assemble().finalize().extrude(-200).union(w1.workplane(offset=-120/2).box(12,18,120))