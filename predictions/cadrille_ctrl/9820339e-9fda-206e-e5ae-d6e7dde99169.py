import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,20))
r=w0.sketch().segment((-29,-7),(-29,7)).arc((-30,0),(-29,-7)).assemble().finalize().extrude(-40).union(w0.sketch().segment((24,-6),(24,0)).segment((30,0)).arc((-28,9),(29,-6)).close().assemble().circle(3,mode='s').finalize().extrude(-20))
