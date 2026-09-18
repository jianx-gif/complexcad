import cadquery as cq
w0=cq.Workplane('YZ',origin=(-76,0,0))
w1=cq.Workplane('ZX',origin=(0,44,0))
r=w0.sketch().circle(100).circle(99,mode='s').finalize().extrude(176).union(w1.sketch().arc((-61,-38),(-39,-46),(-23,-63)).arc((70,42),(-61,-38)).assemble().finalize().extrude(-33))