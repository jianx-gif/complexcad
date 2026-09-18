import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-61,0))
r=w0.workplane(offset=-3/2).cylinder(3,98).union(w0.sketch().circle(100).circle(99,mode='s').finalize().extrude(15)).union(w0.sketch().arc((1,1),(17,2),(32,6)).arc((29,31),(29,56)).arc((17,31),(1,10)).close().assemble().finalize().extrude(125))