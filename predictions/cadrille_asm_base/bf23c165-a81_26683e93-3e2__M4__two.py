import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-11))
w1=cq.Workplane('ZX',origin=(0,25,0))
r=w0.sketch().segment((-63,-100),(66,-100)).segment((66,61)).segment((-32,61)).segment((-32,100)).segment((-39,100)).segment((-39,61)).segment((-63,61)).close().assemble().push([(-40,11)]).circle(10,mode='s').push([(1,-20)]).circle(52,mode='s').finalize().extrude(6).union(w0.workplane(offset=16/2).moveTo(1.5,-19.5).box(49,47,16)).union(w1.sketch().segment((-13,-66),(11,-66)).segment((11,63)).segment((-13,63)).segment((-13,1)).arc((3,-20),(-13,-42)).close().assemble().finalize().extrude(40))