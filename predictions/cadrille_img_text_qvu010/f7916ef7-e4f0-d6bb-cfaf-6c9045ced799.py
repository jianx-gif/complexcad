import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-29,0))
w1=cq.Workplane('YZ',origin=(-89,0,0))
r=w0.sketch().circle(53).circle(42,mode='s').finalize().extrude(64).union(w0.sketch().segment((-26,72),(26,72)).arc((0,75),(-26,72)).assemble().finalize().extrude(129)).union(w1.sketch().arc((-100,-30),(-67,-77),(-19,-100)).segment((-19,-99)).arc((-25,-94),(-30,-89)).segment((-30,89)).arc((-35,84),(-40,79)).arc((-44,79),(-48,78)).arc((-74,55),(-100,35)).close().assemble().finalize().extrude(189))