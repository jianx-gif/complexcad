import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,2))
r=w0.sketch().segment((-93,-62),(-91,-62)).arc((-77,-57),(-64,-62)).segment((-12,-62)).segment((-12,-64)).segment((93,-64)).arc((1,84),(-93,-62)).assemble().finalize().extrude(-24).union(w0.sketch().push([(0,-64)]).circle(36).circle(13,mode='s').finalize().extrude(20))