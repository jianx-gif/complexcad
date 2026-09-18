import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-72,0))
r=w0.sketch().segment((-44,19),(-22,-26)).segment((44,5)).segment((22,50)).close().assemble().finalize().extrude(52).union(w0.sketch().circle(100).circle(44,mode='s').push([(61,2)]).rect(22,126,mode='s').finalize().extrude(144))