import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,44,0))
w1=cq.Workplane('XY',origin=(0,0,63))
r=w0.sketch().arc((-63,-71),(15,-39),(44,35)).segment((44,36)).arc((16,-37),(-63,-59)).close().assemble().finalize().extrude(-144).union(w0.sketch().arc((39,96),(-61,-59),(62,80)).arc((45,80),(39,96)).assemble().finalize().extrude(56)).union(w1.sketch().arc((-71,39),(15,68),(95,19)).arc((16,99),(-71,39)).assemble().finalize().extrude(-66))