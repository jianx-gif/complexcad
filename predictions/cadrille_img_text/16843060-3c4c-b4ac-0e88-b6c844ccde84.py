import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-33,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().push([(0,12)]).circle(13).circle(10,mode='s').finalize().extrude(83).union(w1.sketch().segment((-100,-39),(-90,-39)).arc((0,-92),(90,-39)).segment((100,-39)).segment((100,-17)).arc((0,-89),(-100,-17)).close().assemble().finalize().extrude(-200))