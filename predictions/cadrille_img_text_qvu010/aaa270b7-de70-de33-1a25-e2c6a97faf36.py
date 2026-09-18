import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-58,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().arc((-82,-31),(0,-84),(82,-31)).segment((24,-31)).arc((0,-42),(-24,-31)).close().assemble().reset().face(w0.sketch().segment((-82,31),(-24,31)).arc((0,42),(24,31)).segment((82,31)).arc((0,84),(-82,31)).assemble()).finalize().extrude(131).union(w1.sketch().circle(100).push([(-50,-4)]).circle(18,mode='s').push([(0,0)]).circle(25,mode='s').finalize().extrude(139))