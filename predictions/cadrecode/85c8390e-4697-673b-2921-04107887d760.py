import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-33))
r=w0.sketch().segment((-76,-69),(-71,-69)).arc((0,-100),(71,-69)).segment((76,-69)).segment((76,-65)).arc((100,0),(76,65)).segment((76,69)).segment((71,69)).arc((0,100),(-71,69)).segment((-76,69)).segment((-76,65)).arc((-100,0),(-76,-65)).close().assemble().finalize().extrude(66).union(w0.workplane(offset=66/2).cylinder(66,90))