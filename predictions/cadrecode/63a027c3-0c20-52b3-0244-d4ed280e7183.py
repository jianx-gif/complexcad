import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,9))
r=w0.sketch().circle(100).push([(-92,1)]).circle(5,mode='s').push([(-65,-69)]).circle(7,mode='s').push([(0,89)]).circle(3,mode='s').push([(65,67)]).circle(6,mode='s').push([(92,-1)]).circle(5,mode='s').finalize().extrude(-31).union(w0.sketch().circle(46).circle(9,mode='s').finalize().extrude(13))