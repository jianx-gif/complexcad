import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-89,0))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().arc((-89,-48),(-88,-49),(-87,-50)).segment((-87,-48)).close().assemble().reset().face(w0.sketch().arc((-86,-51),(-79,-56),(-71,-58)).segment((-71,-51)).close().assemble()).reset().face(w0.sketch().arc((-69,-58),(1,-6),(89,-1)).segment((89,58)).segment((-69,58)).close().assemble()).finalize().extrude(179).union(w1.sketch().arc((-75,-84),(-12,-12),(75,-60)).arc((-15,89),(-75,-84)).assemble().finalize().extrude(200))