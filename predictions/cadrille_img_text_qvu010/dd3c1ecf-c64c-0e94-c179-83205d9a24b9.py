import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-18,0))
w1=cq.Workplane('XY',origin=(0,0,-92))
r=w0.sketch().rect(200,198).push([(-87,0)]).circle(13,mode='s').push([(0,0)]).circle(53,mode='s').push([(87,0)]).circle(13,mode='s').finalize().extrude(35).union(w1.sketch().arc((-69,-21),(0,-60),(69,-21)).segment((48,-21)).arc((0,-49),(-48,-21)).close().assemble().finalize().extrude(160))