import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
w1=cq.Workplane('ZX',origin=(0,0,0))
r=w0.sketch().segment((-30,-16),(-22,-16)).segment((-22,-29)).segment((15,-29)).segment((15,-16)).segment((23,-16)).segment((23,-14)).segment((30,-14)).segment((30,14)).segment((23,14)).segment((23,16)).segment((15,16)).segment((15,31)).segment((-22,31)).segment((-22,16)).segment((-30,16)).segment((-30,14)).segment((-38,14)).segment((-38,-14)).segment((-30,-14)).close().assemble().finalize().extrude(2).union(w0.sketch().circle(12).circle(11,mode='s').finalize().extrude(20)).union(w1.sketch().circle(40).circle(30,mode='s').finalize().extrude(8))
