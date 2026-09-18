import cadquery as cq
w0=cq.Workplane('YZ',origin=(87,0,0))
w1=cq.Workplane('ZX',origin=(0,95,0))
r=w0.sketch().segment((-95,-31),(-89,-31)).arc((0,-94),(89,-31)).segment((95,-31)).segment((95,31)).segment((89,31)).arc((0,94),(-89,31)).segment((-95,31)).close().assemble().push([(0,1)]).circle(81,mode='s').finalize().extrude(-10).union(w1.sketch().arc((-4,-100),(54,0),(-4,100)).segment((-4,66)).arc((33,0),(-4,-66)).close().assemble().finalize().extrude(-151))