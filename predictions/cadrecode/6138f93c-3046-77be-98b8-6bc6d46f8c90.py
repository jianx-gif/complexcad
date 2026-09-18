import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,79))
w1=cq.Workplane('ZX',origin=(0,-27,0))
r=w0.workplane(offset=-179/2).moveTo(3,0).cylinder(179,40).union(w0.sketch().push([(3,0)]).circle(47).circle(3,mode='s').finalize().extrude(-110)).union(w0.sketch().segment((-53,-1),(-48,-1)).segment((-48,-37)).segment((53,-34)).segment((52,38)).segment((-48,38)).segment((-48,1)).segment((-53,1)).close().assemble().finalize().extrude(11)).union(w1.sketch().push([(3,0)]).circle(48).circle(46,mode='s').finalize().extrude(65))