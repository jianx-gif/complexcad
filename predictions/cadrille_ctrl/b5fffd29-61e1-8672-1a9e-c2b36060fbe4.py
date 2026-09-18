import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,10))
r=w0.sketch().segment((-40,-30),(40,-30)).segment((40,30)).segment((13,30)).arc((-9,-14),(-40,21)).close().assemble().finalize().extrude(-10).union(w0.sketch().segment((-30,-17),(-24,-17)).segment((-24,-30)).segment((24,-30)).segment((24,-17)).segment((30,-17)).segment((30,17)).segment((24,17)).segment((24,30)).segment((-24,30)).segment((-24,17)).segment((-30,17)).close().assemble().circle(16,mode='s').finalize().extrude(-10))
