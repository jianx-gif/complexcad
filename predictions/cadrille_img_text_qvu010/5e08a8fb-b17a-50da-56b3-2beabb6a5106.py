import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,99,0))
w1=cq.Workplane('ZX',origin=(0,77,0))
r=w0.sketch().segment((-83,-50),(83,-50)).segment((83,40)).segment((-83,50)).close().assemble().finalize().extrude(-156).union(w0.sketch().arc((-58,-29),(0,-71),(58,-29)).close().assemble().reset().face(w0.sketch().segment((-58,29),(58,29)).arc((0,71),(-58,29)).assemble()).finalize().extrude(-155)).union(w1.sketch().segment((-100,-85),(100,-85)).segment((100,85)).segment((-100,85)).segment((-100,-19)).arc((-96,-36),(-100,-53)).close().assemble().circle(17,mode='s').finalize().extrude(-135))