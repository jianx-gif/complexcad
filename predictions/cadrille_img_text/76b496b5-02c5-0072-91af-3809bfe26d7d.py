import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-33,0))
w1=cq.Workplane('YZ',origin=(-95,0,0))
r=w0.sketch().arc((-43,-86),(-33,-89),(-23,-91)).close().assemble().finalize().extrude(71).union(w1.sketch().arc((-80,-11),(-54,43),(-11,80)).segment((-11,100)).segment((11,100)).segment((11,80)).arc((33,73),(54,63)).arc((49,65),(44,67)).segment((44,94)).segment((-44,94)).segment((-44,67)).arc((-67,31),(-80,-11)).assemble().finalize().extrude(195))