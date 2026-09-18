import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-16,0))
w1=cq.Workplane('ZX',origin=(0,73,0))
r=w0.sketch().circle(100).reset().face(w0.sketch().segment((-80,10),(-69,-25)).segment((-58,-22)).arc((-67,-4),(-69,15)).close().assemble(),mode='s').reset().face(w0.sketch().arc((58,22),(67,4),(69,-15)).segment((80,-10)).segment((69,25)).close().assemble(),mode='s').finalize().extrude(31).union(w1.sketch().arc((19,-72),(44,-61),(65,-43)).arc((-43,60),(19,-72)).assemble().finalize().extrude(-146))