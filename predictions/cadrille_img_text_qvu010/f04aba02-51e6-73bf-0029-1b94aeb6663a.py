import cadquery as cq
w0=cq.Workplane('YZ',origin=(-68,0,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().arc((-90,-42),(0,-85),(90,-42)).segment((84,-42)).arc((0,-84),(-84,-42)).close().assemble().reset().face(w0.sketch().segment((-90,42),(-84,42)).arc((0,84),(84,42)).segment((90,42)).arc((0,85),(-90,42)).assemble()).finalize().extrude(148).union(w1.sketch().push([(-5.5,0)]).rect(185,52).push([(-6,0)]).circle(30,mode='s').finalize().extrude(-192))