import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-38,0))
r=w0.workplane(offset=-56/2).box(24,28,56).union(w0.sketch().circle(97).circle(53,mode='s').finalize().extrude(10)).union(w0.sketch().arc((19,-79),(57,-63),(86,-35)).segment((100,-35)).arc((-79,62),(19,-79)).assemble().finalize().extrude(112))