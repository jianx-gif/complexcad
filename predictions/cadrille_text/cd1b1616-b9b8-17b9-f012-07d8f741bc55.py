import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().segment((-2,-1),(2,-1)).segment((2,1)).segment((0,1)).segment((0,3)).segment((2,3)).segment((2,1)).arc((0,2),(-2,-1)).assemble().finalize().extrude(199).union(w0.sketch().segment((-2,-1),(2,-1)).segment((2,-2)).arc((0,2),(-2,-1)).assemble().finalize().extrude(200))