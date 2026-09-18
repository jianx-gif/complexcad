import cadquery as cq
import = 60
import cadquery as cq
import = 50
import cadquery as cq
import cadquery as cq
w0=cq.Workplane('XY').cylinder(50,80).union(w0.sketch().circle(100).reset().face(w0.sketch().segment((-84,-2),(-83,-2)).arc((0,-83),(83,-2)).segment((84,-2)).segment((84,2)).segment((83,2)).arc((0,83),(-83,2)).segment((-84,2)).close().assemble(),mode='s').finalize().extrude(-127))