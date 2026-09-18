import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
w1=cq.Workplane('XY',origin=(0,0,20))
r=w0.sketch().segment((-22,-38),(22,-38)).segment((22,-17)).arc((27,0),(22,17)).segment((22,38)).segment((-22,38)).segment((-22,17)).arc((-27,0),(-22,-17)).close().assemble().finalize().extrude(-3).union(w0.sketch().rect(80,50).rect(16,38,mode='s').finalize().extrude(2)).union(w1.sketch().rect(80,50).circle(25,mode='s').finalize().extrude(-20))
