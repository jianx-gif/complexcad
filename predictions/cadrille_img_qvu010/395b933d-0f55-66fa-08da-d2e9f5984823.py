import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,52,0))
w1=cq.Workplane('YZ',origin=(46,0,0))
r=w0.sketch().circle(100).circle(99,mode='s').finalize().extrude(-121).union(w0.sketch().arc((-89,-21),(0,-81),(89,-21)).segment((74,-21)).arc((77,0),(74,21)).segment((89,21)).arc((0,81),(-89,21)).segment((-74,21)).arc((-77,0),(-74,-21)).close().assemble().finalize().extrude(48)).union(w1.sketch().arc((38,-100),(40,-98),(42,-97)).segment((38,-97)).close().assemble().finalize().extrude(-133))