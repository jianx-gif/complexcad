import cadquery as cq
w0=cq.Workplane('YZ',origin=(-40,0,0))
r=w0.sketch().push([(0,49.5)]).rect(78,97).push([(0,49)]).rect(76,98,mode='s').finalize().extrude(78).union(w0.sketch().push([(0,50)]).rect(80,100).rect(76,74,mode='s').finalize().extrude(80))
