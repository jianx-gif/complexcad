import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,33,0))
r=w0.workplane(offset=-83/2).cylinder(83,38).union(w0.workplane(offset=-33/2).cylinder(33,58)).union(w0.workplane(offset=17/2).cylinder(17,100))