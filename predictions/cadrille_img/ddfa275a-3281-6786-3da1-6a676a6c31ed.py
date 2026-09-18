import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-89,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().circle(96).reset().face(w0.sketch().arc((-50,29),(-60,-41),(-1,-79)).arc((78,46),(-50,29)).assemble(),mode='s').finalize().extrude(149).union(w0.sketch().arc((-29,-55),(1,-60),(30,-51)).arc((46,-18),(65,13)).arc((29,43),(17,89)).arc((-35,33),(-29,-55)).assemble().finalize().extrude(189)).union(w1.sketch().circle(75).push([(11,26)]).circle(56,mode='s').finalize().extrude(164))