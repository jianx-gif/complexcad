import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().segment((-39,-2),(-20,-2)).segment((-20,-34)).segment((21,-34)).segment((21,-2)).segment((39,-2)).segment((39,2)).segment((21,2)).segment((21,34)).segment((-20,34)).segment((-20,2)).segment((-39,2)).close().assemble().finalize().extrude(20).union(w0.workplane(offset=80/2).cylinder(80,32))