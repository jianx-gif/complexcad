import cadquery as cq
w0=cq.Workplane('YZ',origin=(-78,0,0))
w1=cq.Workplane('YZ',origin=(-100,0,0))
r=w0.sketch().circle(96).push([(12,31)]).circle(44,mode='s').finalize().extrude(174).union(w1.sketch().arc((-61,-77),(0,-97),(61,-77)).segment((61,-76)).arc((100,0),(61,76)).segment((61,77)).segment((-61,77)).segment((-61,76)).arc((-100,0),(-61,-76)).close().assemble().circle(95,mode='s').finalize().extrude(200))