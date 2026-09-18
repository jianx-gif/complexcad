import cadquery as cq
w0=cq.Workplane('YZ',origin=(-40,0,0))
r=w0.sketch().push([(0,49.5)]).rect(76,97).push([(0,49)]).circle(46,mode='s').finalize().extrude(78).union(w0.sketch().push([(0,50)]).rect(80,100).rect(76,96,mode='s').finalize().extrude(80))