import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,22))
r=w0.sketch().push([(-5,0)]).rect(190,120).rect(180,110,mode='s').finalize().extrude(-47).union(w0.sketch().arc((98,-10),(100,0),(98,10)).close().assemble().finalize().extrude(3))