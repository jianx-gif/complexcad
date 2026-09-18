import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-77,0))
r=w0.sketch().circle(100).circle(49,mode='s').finalize().extrude(-13).union(w0.sketch().circle(99).circle(48,mode='s').finalize().extrude(48)).union(w0.sketch().arc((-79,-19),(-45,-52),(-10,-82)).arc((41,-49),(79,-2)).arc((42,36),(35,86)).arc((-42,59),(-79,-19)).assemble().finalize().extrude(168))