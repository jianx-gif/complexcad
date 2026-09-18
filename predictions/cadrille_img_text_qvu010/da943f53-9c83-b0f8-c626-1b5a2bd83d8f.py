import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-38,0))
r=w0.sketch().circle(100).circle(26,mode='s').finalize().extrude(17).union(w0.sketch().segment((-72,46),(-29,-46)).segment((72,-46)).segment((29,46)).close().assemble().finalize().extrude(77))