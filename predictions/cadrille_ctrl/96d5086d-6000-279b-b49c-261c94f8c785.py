import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,16))
w1=cq.Workplane('ZX',origin=(0,10,0))
r=w0.sketch().segment((-40,10),(-39,10)).segment((-39,11)).segment((-40,11)).close().assemble().finalize().extrude(-16).union(w0.sketch().segment((-34,1),(-33,-10)).segment((-24,-9)).segment((-24,-8)).segment((-23,-8)).segment((-23,-7)).segment((-22,-7)).segment((-23,4)).segment((-32,3)).segment((-32,1)).close().assemble().finalize().extrude(-16)).union(w0.sketch().segment((15,-10),(49,-5)).segment((44,11)).close().assemble().finalize().extrude(-16)).union(w0.workplane(offset=8/2).moveTo(29,0).cylinder(8,1))
