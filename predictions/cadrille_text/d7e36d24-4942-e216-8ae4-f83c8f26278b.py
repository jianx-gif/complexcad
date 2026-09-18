import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().segment((-88,12),(-88,14)).arc((-87,16),(-85,18)).segment((-85,19)).arc((-87,16),(-88,12)).assemble().finalize().extrude(200).union(w0.sketch().segment((23,-58),(29,-58)).segment((29,-55)).arc((26,-56),(23,-58)).assemble().finalize().extrude(200))