import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,8))
r=w0.sketch().segment((-81,100),(-80,-100)).segment((72,-100)).segment((72,-74)).segment((-54,-74)).segment((-54,100)).close().assemble().push([(34,-95)]).circle(4,mode='s').finalize().extrude(-22).union(w0.workplane(offset=6/2).moveTo(76,-70).cylinder(6,7))