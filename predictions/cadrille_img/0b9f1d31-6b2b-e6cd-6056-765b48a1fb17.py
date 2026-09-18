import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
w1=cq.Workplane('XY',origin=(0,0,23))
r=w0.sketch().segment((-85,-21),(1,-76)).segment((85,43)).segment((-1,98)).arc((-38,46),(-85,2)).close().assemble().finalize().extrude(-186).union(w0.sketch().arc((-1,-98),(19,0),(-1,98)).close().assemble().finalize().extrude(-198)).union(w1.sketch().push([(0,24)]).circle(33).circle(27,mode='s').finalize().extrude(-57))