import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('XY',origin=(0,0,-97))
r=w0.sketch().circle(100).circle(97,mode='s').finalize().extrude(200).union(w1.sketch().arc((-3,-3),(0,-2),(3,-3)).segment((3,3)).segment((-3,3)).close().assemble().finalize().extrude(197))