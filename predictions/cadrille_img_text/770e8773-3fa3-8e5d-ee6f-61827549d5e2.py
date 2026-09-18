import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-67,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().arc((-39,-96),(11,-68),(55,-29)).arc((58,-26),(61,-23)).arc((66,-12),(72,-1)).arc((69,1),(66,3)).arc((44,58),(-10,85)).close().assemble().finalize().extrude(121).union(w1.sketch().arc((-19,34),(-51,-49),(35,-33)).arc((49,58),(-19,34)).assemble().finalize().extrude(200))