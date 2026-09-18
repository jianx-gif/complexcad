import cadquery as cq
w0=cq.Workplane('YZ',origin=(34,0,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().circle(99).reset().face(w0.sketch().segment((-98,-19),(-95,-21)).arc((-89,-38),(-76,-52)).segment((-76,-54)).segment((-74,-54)).arc((38,-71),(95,19)).segment((98,19)).segment((95,21)).arc((89,38),(76,52)).segment((76,54)).segment((74,54)).arc((-38,71),(-95,-19)).close().assemble(),mode='s').finalize().extrude(-109).union(w1.sketch().arc((-99,-42),(-65,-49),(-53,-81)).arc((79,58),(-99,-42)).assemble().finalize().extrude(200))