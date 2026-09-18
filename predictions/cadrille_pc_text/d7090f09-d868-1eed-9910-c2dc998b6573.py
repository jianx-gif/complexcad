import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,32))
w1=cq.Workplane('XY',origin=(0,0,28))
r=w0.sketch().segment((-74,-62),(-69,-62)).arc((0,-88),(69,-62)).segment((74,-62)).segment((74,-55)).arc((88,0),(74,55)).segment((74,62)).segment((69,62)).arc((0,88),(-69,62)).segment((-74,62)).segment((-74,55)).arc((-88,0),(-74,-55)).close().assemble().circle(82,mode='s').finalize().extrude(-71).union(w1.sketch().arc((-39,50),(1,53),(39,48)).segment((39,100)).segment((-39,100)).close().assemble().push([(-12,77)]).circle(10,mode='s').finalize().extrude(11))