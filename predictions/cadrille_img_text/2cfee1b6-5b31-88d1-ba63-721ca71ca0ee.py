import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-61))
w1=cq.Workplane('ZX',origin=(0,86,0))
r=w0.sketch().arc((-87,50),(86,-51),(-82,60)).segment((-82,50)).close().assemble().finalize().extrude(151).union(w1.sketch().push([(0,8)]).circle(92).circle(73,mode='s').finalize().extrude(-149))