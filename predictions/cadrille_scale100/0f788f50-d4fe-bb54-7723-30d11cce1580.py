import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,8))
w1=cq.Workplane('YZ',origin=(30,0,0))
r=w0.sketch().push([(0,-1)]).rect(80,58).push([(0,-1.5)]).rect(58,33,mode='s').finalize().extrude(-8).union(w0.sketch().push([(0,-1)]).circle(20).circle(15,mode='s').finalize().extrude(-8)).union(w1.workplane(offset=-59/2).moveTo(0,0.5).box(30,7,59))