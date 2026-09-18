import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-14,0))
w1=cq.Workplane('YZ',origin=(-100,0,0))
r=w0.sketch().circle(95).circle(67,mode='s').finalize().extrude(29).union(w0.sketch().segment((-49,-76),(-45,-81)).segment((-39,-76)).close().assemble().finalize().extrude(114)).union(w1.sketch().arc((-100,-48),(59,-72),(48,78)).segment((48,59)).arc((56,-59),(-73,-48)).close().assemble().finalize().extrude(172))