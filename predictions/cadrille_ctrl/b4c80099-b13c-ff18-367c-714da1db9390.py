import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,12))
w1=cq.Workplane('XY',origin=(0,0,22))
r=w0.sketch().segment((-40,-18),(-27,-18)).segment((-27,-34)).segment((27,-34)).segment((27,-18)).segment((40,-18)).segment((40,18)).segment((27,18)).segment((27,34)).segment((-27,34)).segment((-27,18)).segment((-40,18)).close().assemble().finalize().extrude(-12).union(w0.sketch().circle(43).circle(28,mode='s').finalize().extrude(6)).union(w1.sketch().circle(43).circle(31,mode='s').finalize().extrude(-20))
