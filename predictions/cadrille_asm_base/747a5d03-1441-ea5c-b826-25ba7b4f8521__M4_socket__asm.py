import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-45))
w1=cq.Workplane('ZX',origin=(0,-25,0))
r=w0.sketch().circle(100).circle(37,mode='s').push([(82,-3)]).circle(7,mode='s').finalize().extrude(75).union(w0.sketch().arc((87,3),(88,2),(88,1)).segment((90,3)).close().assemble().finalize().extrude(90)).union(w1.sketch().arc((-24,-10),(-1,16),(-24,42)).close().assemble().finalize().extrude(43))