import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,43))
w1=cq.Workplane('XY',origin=(0,0,74))
r=w0.workplane(offset=-143/2).cylinder(143,6).union(w0.sketch().circle(57).push([(-49,0)]).circle(5,mode='s').push([(0,0)]).rect(10,92,mode='s').push([(49,0)]).rect(10,8,mode='s').finalize().extrude(-77)).union(w0.sketch().circle(69).circle(57,mode='s').finalize().extrude(26)).union(w1.sketch().push([(0,3)]).circle(29).circle(4,mode='s').finalize().extrude(26))