import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,35,0))
w1=cq.Workplane('XY',origin=(0,0,-50))
r=w0.sketch().push([(0,-1)]).rect(200,198).circle(92,mode='s').finalize().extrude(-16).union(w1.sketch().arc((-56,-47),(0,-89),(56,-47)).segment((48,-47)).arc((0,-71),(-48,-47)).close().assemble().finalize().extrude(104))