import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,53,0))
r=w0.sketch().circle(33).circle(20,mode='s').finalize().extrude(-120).union(w0.sketch().arc((-99,-12),(99,0),(-99,12)).arc((-100,0),(-99,-12)).assemble().finalize().extrude(14))