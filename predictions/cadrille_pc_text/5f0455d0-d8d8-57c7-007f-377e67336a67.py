import cadquery as cq
w0=cq.Workplane('YZ',origin=(69,0,0))
w1=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().push([(0,-8.5)]).rect(92,69).push([(-29,-3)]).circle(6,mode='s').push([(28,-3)]).circle(6,mode='s').finalize().extrude(-169).union(w1.workplane(offset=-29/2).moveTo(0,25.5).box(58,35,29))