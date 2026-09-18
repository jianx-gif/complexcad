import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,8))
r=w0.sketch().segment((-35,-25),(-34,-25)).segment((-34,-50)).segment((35,-50)).segment((35,50)).segment((-35,50)).close().assemble().push([(-22,9)]).circle(8,mode='s').finalize().extrude(-8).union(w0.sketch().segment((-23,6),(23,-7)).segment((23,7)).segment((-23,7)).close().assemble().finalize().extrude(4))
