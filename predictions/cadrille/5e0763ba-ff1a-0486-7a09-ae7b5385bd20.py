import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-15))
r=w0.sketch().segment((-100,-37),(-54,-37)).segment((-54,-35)).segment((-51,-35)).segment((-51,-37)).segment((100,-37)).segment((100,10)).segment((44,20)).segment((52,1)).segment((40,-5)).segment((32,15)).segment((35,20)).segment((-100,37)).close().assemble().finalize().extrude(30)