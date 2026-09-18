import cadquery as cq
w0=cq.Workplane('YZ',origin=(-100,0,0))
w1=cq.Workplane('YZ',origin=(-93,0,0))
r=w0.sketch().segment((-53,-38),(53,-38)).segment((53,38)).segment((-53,38)).segment((-53,37)).segment((-51,37)).segment((-51,35)).segment((-53,35)).close().assemble().finalize().extrude(200).union(w1.sketch().circle(42).circle(39,mode='s').finalize().extrude(157))