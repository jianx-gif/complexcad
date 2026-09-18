import cadquery as cq
w0=cq.Workplane('YZ',origin=(-1,0,0))
w1=cq.Workplane('YZ',origin=(-39,0,0))
r=w0.sketch().segment((-69,-70),(-69,-68)).segment((-66,-68)).segment((-66,-72)).arc((68,73),(-69,-70)).assemble().circle(97,mode='s').finalize().extrude(-18).union(w1.sketch().circle(100).circle(99,mode='s').finalize().extrude(82))