import cadquery as cq
import = 60
import cadquery as cq
import cadquery as cq
w0=cq.Workplane('XY').r=w0.sketch().circle(86).circle(80,mode='s').finalize().extrude(-160).union(w0.sketch().circle(100).circle(80,mode='s').finalize().extrude(100))