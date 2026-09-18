import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().segment((17,13),(17,15)).arc((16,14),(17,13)).assemble().finalize().extrude(-50).union(w0.sketch().arc((24,-18),(11,0),(29,-10)).arc((-26,15),(24,-18)).assemble().push([(0,0)]).circle(3,mode='s').finalize().extrude(50)).union(w0.workplane(offset=50/2).moveTo(0,0.5).box(40,15,50))