import cadquery as cq
w0=cq.Workplane('YZ',origin=(100,0,0))
r=w0.workplane(offset=-200/2).moveTo(0,-2.5).box(150,9,200).union(w0.workplane(offset=-74/2).moveTo(0,2.5).box(20,11,74))