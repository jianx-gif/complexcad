import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-47,0))
w1=cq.Workplane('XY',origin=(0,0,25))
r=w0.sketch().arc((-67,-49),(-61,-78),(-49,-100)).arc((-3,-76),(43,-49)).segment((43,-37)).segment((64,-37)).arc((67,-32),(67,-27)).segment((67,98)).segment((43,98)).segment((43,78)).arc((-42,44),(-58,-49)).close().assemble().finalize().extrude(77).union(w0.sketch().arc((-15,-87),(29,-58),(34,-5)).close().assemble().finalize().extrude(94)).union(w1.sketch().push([(31,-3)]).circle(69).push([(3,-13)]).circle(8,mode='s').finalize().extrude(42))