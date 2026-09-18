import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,4))
w1=cq.Workplane('YZ',origin=(60,0,0))
r=w0.workplane(offset=-16/2).cylinder(16,4).union(w0.workplane(offset=-8/2).moveTo(79,0).box(42,20,8)).union(w1.sketch().push([(0,6)]).rect(60,12).push([(0,5)]).circle(5,mode='s').finalize().extrude(-160))