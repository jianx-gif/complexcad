import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-38,0))
w1=cq.Workplane('ZX',origin=(0,-87,0))
r=w0.sketch().segment((-68,36),(-66,34)).arc((-63,29),(-59,25)).arc((50,-45),(43,76)).arc((43,80),(42,84)).segment((44,86)).segment((42,88)).arc((19,98),(-6,99)).segment((-8,100)).segment((-9,98)).arc((-45,75),(-65,38)).close().assemble().finalize().extrude(124).union(w1.sketch().arc((-59,-46),(58,-60),(95,45)).arc((88,42),(88,49)).arc((-15,69),(-59,-19)).close().assemble().finalize().extrude(175))