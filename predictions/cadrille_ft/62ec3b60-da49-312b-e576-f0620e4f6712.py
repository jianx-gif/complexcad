import cadquery as cq
import = 50
import cadquery as cq
import cadquery as cq
import cadquery as cq
import cadquery as cq
w0=cq.Workplane('XY').r=w0.workplane(offset=-77).box(100,100,77).union(w0.sketch().circle(100).reset().face(w0.sketch().segment((-36,-50),(-36,50)).arc((-59,0),(-36,-50)).assemble(),mode='s').reset().face(w0.sketch().arc((36,-50),(59,0),(36,50)).close().assemble(),mode='s').finalize().extrude(37))