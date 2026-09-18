import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,99,0))
w1=cq.Workplane('ZX',origin=(0,73,0))
r=w0.sketch().arc((-46,-69),(0,-86),(46,-69)).segment((39,-69)).arc((0,-82),(-39,-69)).close().assemble().reset().face(w0.sketch().segment((-46,69),(-39,69)).arc((0,82),(39,69)).segment((46,69)).arc((0,86),(-46,69)).assemble()).finalize().extrude(-198).union(w1.sketch().segment((-69,-72),(-69,-69)).arc((0,-86),(69,-69)).segment((69,-72)).arc((100,0),(69,72)).segment((69,69)).arc((0,86),(-69,69)).segment((-69,72)).arc((-100,0),(-69,-72)).assemble().circle(86,mode='s').finalize().extrude(-147))