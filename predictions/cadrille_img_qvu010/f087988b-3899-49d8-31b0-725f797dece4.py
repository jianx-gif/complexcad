import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,14,0))
w1=cq.Workplane('ZX',origin=(0,45,0))
r=w0.sketch().circle(100).circle(61,mode='s').circle(41).finalize().extrude(-18).union(w0.sketch().segment((-11,11),(11,11)).arc((0,13),(-11,11)).assemble().reset().face(w0.sketch().arc((12,-13),(13,-8),(12,-3)).close().assemble()).finalize().extrude(64)).union(w1.sketch().segment((-11,-70),(11,-70)).segment((11,-69)).arc((69,0),(11,69)).segment((11,70)).segment((-11,70)).segment((-11,69)).arc((-69,0),(-11,-69)).close().assemble().finalize().extrude(-122))