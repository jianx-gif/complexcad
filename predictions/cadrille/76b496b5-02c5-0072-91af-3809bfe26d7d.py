import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-14))
w1=cq.Workplane('XY',origin=(0,0,-2))
r=w0.sketch().segment((-81,100),(-80,-100)).segment((72,-100)).segment((72,-74)).segment((-54,-74)).segment((-55,100)).close().assemble().push([(34,-95)]).circle(4,mode='s').finalize().extrude(22).union(w1.sketch().arc((72,-64),(73,-69),(73,-74)).segment((81,-74)).segment((81,-64)).close().assemble().finalize().extrude(16))