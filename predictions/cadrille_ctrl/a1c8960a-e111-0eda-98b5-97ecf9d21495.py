import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,10))
r=w0.sketch().arc((-39,1),(-38,-12),(-30,-23)).arc((-29,-27),(-26,-31)).segment((-26,-30)).arc((-29,-17),(-26,-4)).segment((-26,4)).segment((-24,4)).arc((-1,24),(22,4)).segment((24,4)).segment((24,-4)).arc((27,-17),(24,-30)).segment((24,-33)).arc((20,34),(-39,1)).assemble().finalize().extrude(-10).union(w0.sketch().push([(0,-1)]).circle(39).circle(31,mode='s').finalize().extrude(-10)).union(w0.workplane(offset=4/2).moveTo(0,-1).cylinder(4,15))
