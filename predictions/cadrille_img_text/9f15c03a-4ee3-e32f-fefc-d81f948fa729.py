import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-30,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().arc((-34,16),(-2,20),(29,28)).segment((29,45)).segment((45,45)).arc((46,50),(47,55)).arc((6,-59),(-34,54)).close().assemble().finalize().extrude(120).union(w1.sketch().arc((-85,-55),(0,-100),(85,-55)).segment((34,-55)).arc((0,-62),(-34,-55)).close().assemble().push([(33,-17)]).rect(24,28,mode='s').finalize().extrude(-172))