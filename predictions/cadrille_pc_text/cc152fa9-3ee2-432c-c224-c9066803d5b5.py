import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,13))
r=w0.sketch().circle(100).circle(52,mode='s').finalize().extrude(-13).union(w0.sketch().circle(45).push([(35,-11)]).circle(10,mode='s').finalize().extrude(-10)).union(w0.workplane(offset=1/2).cylinder(1,8))