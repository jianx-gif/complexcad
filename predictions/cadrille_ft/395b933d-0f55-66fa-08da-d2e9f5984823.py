import cadquery as cq
import = 80
import cadquery as cq
import = 80
import cadquery as cq
import cadquery as cq
w0=cq.Workplane('XY').r=w0.sketch().push([(-95,-50)]).rect(10,100).push([(95,50)]).rect(10,100).finalize().extrude(-107).union(w0.sketch().circle(100).circle(92,mode='s').finalize().extrude(57))