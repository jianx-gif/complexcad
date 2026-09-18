import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-53))
w1=cq.Workplane('ZX',origin=(0,-53,0))
r=w0.sketch().segment((-32,0),(-16,-11)).segment((-15,-10)).segment((-31,1)).close().assemble().finalize().extrude(55).union(w0.sketch().push([(79,0)]).rect(42,32).push([(89,0)]).circle(8,mode='s').finalize().extrude(106)).union(w1.sketch().segment((0,-100),(32,-100)).segment((32,-47)).segment((16,-47)).segment((16,5)).segment((32,5)).segment((32,58)).segment((0,58)).close().assemble().finalize().extrude(106))