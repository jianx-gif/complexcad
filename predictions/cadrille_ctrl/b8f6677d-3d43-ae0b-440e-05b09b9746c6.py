import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,20))
r=w0.sketch().segment((-20,-39),(19,-40)).segment((20,1)).segment((-19,2)).close().assemble().push([(0,-19)]).circle(10,mode='s').finalize().extrude(-20).union(w0.sketch().segment((-19,29),(-18,29)).segment((-18,30)).segment((-19,30)).close().assemble().finalize().extrude(-20)).union(w0.sketch().segment((-19,-16),(19,-16)).segment((19,14)).segment((-19,14)).close().assemble().finalize().extrude(-20))
