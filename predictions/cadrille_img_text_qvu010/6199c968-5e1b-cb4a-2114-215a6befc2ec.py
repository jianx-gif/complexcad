import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-87,0))
r=w0.workplane(offset=18/2).cylinder(18,100).union(w0.sketch().arc((-82,-29),(0,-85),(82,-29)).segment((70,-29)).arc((0,-73),(-70,-29)).close().assemble().reset().face(w0.sketch().segment((-82,29),(-70,29)).arc((0,73),(70,29)).segment((82,29)).arc((0,85),(-82,29)).assemble()).finalize().extrude(187))