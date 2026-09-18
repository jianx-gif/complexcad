import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,90,0))
w1=cq.Workplane('YZ',origin=(-48,0,0))
r=w0.sketch().arc((-75,36),(74,-66),(-17,86)).arc((-47,64),(-75,36)).assemble().finalize().extrude(-153).union(w1.sketch().arc((26,-44),(48,0),(26,44)).close().assemble().finalize().extrude(148))