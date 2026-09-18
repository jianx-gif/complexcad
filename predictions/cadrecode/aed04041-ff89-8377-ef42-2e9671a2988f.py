import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-4))
r=w0.sketch().rect(106,128).rect(46,126,mode='s').finalize().extrude(-5).union(w0.sketch().rect(200,150).push([(-64,-16)]).circle(11,mode='s').push([(0,0)]).rect(72,10,mode='s').push([(57,-21)]).circle(6,mode='s').finalize().extrude(13))