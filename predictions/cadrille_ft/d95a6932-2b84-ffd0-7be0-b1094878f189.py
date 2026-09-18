import cadquery as cq
import = 60
import cadquery as cq
import cadquery as cq
import cadquery as cq
w0=cq.Workplane('XY').cylinder(100,80).union(w0.sketch().circle(82).circle(77,mode='s').finalize().extrude(100))