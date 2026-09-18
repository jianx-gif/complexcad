import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-82,0))
r=w0.workplane(offset=164/2).cylinder(164,90).union(w0.sketch().arc((-70,-41),(0,-80),(70,-41)).segment((39,-41)).arc((0,-53),(-39,-41)).close().assemble().reset().face(w0.sketch().segment((-70,41),(-39,41)).arc((0,53),(39,41)).segment((70,41)).arc((0,80),(-70,41)).assemble()).finalize().extrude(182))