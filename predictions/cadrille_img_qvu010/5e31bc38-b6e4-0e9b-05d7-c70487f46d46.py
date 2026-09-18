import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-22,0))
w1=cq.Workplane('YZ',origin=(11,0,0))
r=w0.sketch().arc((99,-16),(88,0),(100,14)).arc((-100,1),(99,-16)).assemble().finalize().extrude(-28).union(w1.sketch().circle(100).circle(89,mode='s').finalize().extrude(-33))