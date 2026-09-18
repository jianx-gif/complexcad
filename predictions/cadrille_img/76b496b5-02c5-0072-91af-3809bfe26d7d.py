import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-16,0))
w1=cq.Workplane('YZ',origin=(-96,0,0))
r=w0.sketch().arc((-34,-53),(1,-43),(34,-26)).arc((1,-40),(-34,-53)).assemble().finalize().extrude(-64).union(w0.sketch().arc((-89,-49),(-79,-71),(-63,-89)).segment((-63,-87)).segment((-61,-87)).close().assemble().finalize().extrude(85)).union(w1.sketch().segment((-22,-92),(22,-92)).segment((22,-89)).arc((34,-87),(46,-83)).arc((35,-78),(24,-71)).arc((-1,-82),(-22,-92)).assemble().finalize().extrude(196))