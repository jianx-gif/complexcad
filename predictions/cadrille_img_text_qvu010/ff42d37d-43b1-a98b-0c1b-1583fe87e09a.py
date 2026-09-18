import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,48,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-86,-52),(86,-52)).segment((86,52)).segment((-86,52)).segment((-86,15)).segment((-38,15)).segment((-38,-15)).segment((-86,-15)).close().assemble().push([(44,11)]).circle(27,mode='s').finalize().extrude(-40).union(w1.sketch().segment((-79,-18),(79,-18)).segment((79,18)).segment((-79,18)).segment((-79,17)).arc((-76,15),(-79,13)).close().assemble().finalize().extrude(-200))