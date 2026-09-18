import cadquery as cq
w0=cq.Workplane('YZ',origin=(25,0,0))
r=w0.sketch().push([(15,8)]).rect(4,50).push([(15,7.5)]).rect(2,3,mode='s').finalize().extrude(-62).union(w0.sketch().push([(0,4)]).rect(80,8).push([(0,3.5)]).rect(4,5,mode='s').finalize().extrude(-50)).union(w0.workplane(offset=1/2).moveTo(0,4).cylinder(1,3))
