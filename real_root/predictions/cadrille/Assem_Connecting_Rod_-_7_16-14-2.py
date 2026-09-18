import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-61,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().circle(32).circle(24,mode='s').finalize().extrude(-10).union(w0.sketch().segment((-22,-1),(-19,-8)).segment((-19,-10)).segment((-18,-10)).segment((-15,-17)).segment((-13,-15)).arc((7,-20),(19,-3)).segment((22,-2)).segment((19,8)).segment((19,10)).segment((18,10)).segment((15,17)).segment((13,15)).arc((-7,20),(-19,3)).segment((-22,2)).close().assemble().finalize().extrude(161)).union(w1.sketch().circle(24).circle(12,mode='s').finalize().extrude(40))