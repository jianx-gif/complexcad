import cadquery as cq
w0=cq.Workplane('YZ',origin=(100,0,0))
r=w0.workplane(offset=-200/2).moveTo(0,-2.5).box(150,11,200).union(w0.workplane(offset=-75/2).moveTo(0,7).box(20,2,75))