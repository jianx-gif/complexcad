import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,50,0))
w1=cq.Workplane('ZX',origin=(0,33,0))
r=w0.sketch().circle(39).circle(3,mode='s').finalize().extrude(-100).union(w0.workplane(offset=-50/2).cylinder(50,59)).union(w1.sketch().arc((-99,17),(-90,-43),(-48,-87)).segment((-48,-91)).segment((-39,-91)).arc((0,-100),(39,-91)).segment((48,-91)).segment((48,-87)).arc((90,-43),(99,17)).close().assemble().finalize().extrude(17))