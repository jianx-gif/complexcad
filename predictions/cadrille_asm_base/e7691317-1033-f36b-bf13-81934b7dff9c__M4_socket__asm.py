import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,43))
w1=cq.Workplane('XY',origin=(0,0,20))
r=w0.sketch().segment((-16,-5),(16,-5)).segment((16,5)).segment((14,5)).arc((13,3),(12,5)).segment((-16,5)).close().assemble().finalize().extrude(-38).union(w0.sketch().circle(57).circle(46,mode='s').finalize().extrude(57)).union(w1.sketch().circle(86).circle(75,mode='s').finalize().extrude(-120))