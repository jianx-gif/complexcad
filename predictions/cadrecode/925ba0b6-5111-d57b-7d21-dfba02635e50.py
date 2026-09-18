import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,25))
r=w0.sketch().push([(-1,0)]).circle(82).circle(50,mode='s').finalize().extrude(-50).union(w0.sketch().arc((-98,-22),(93,-32),(-70,69)).segment((-70,61)).arc((-91,29),(-98,-9)).segment((-70,-9)).segment((-70,-22)).close().assemble().push([(1,-1)]).circle(89,mode='s').finalize().extrude(-22))