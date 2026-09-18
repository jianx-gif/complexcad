import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,88))
w1=cq.Workplane('ZX',origin=(0,-31,0))
r=w0.sketch().circle(59).circle(53,mode='s').finalize().extrude(-184).union(w0.workplane(offset=-180/2).cylinder(180,54)).union(w1.sketch().arc((49,-70),(100,0),(49,70)).segment((49,38)).arc((93,0),(49,-38)).close().assemble().finalize().extrude(88))