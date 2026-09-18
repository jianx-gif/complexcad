import cadquery as cq
import cadquery as cq
import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-50))
r=w0.sketch().rect(200,200).rect(100,100,mode='s').finalize().extrude(100).union(w0.workplane(offset=100/2).box(100,100,100))