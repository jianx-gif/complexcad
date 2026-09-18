import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-37))
w1=cq.Workplane('YZ',origin=(40,0,0))
r=w0.sketch().circle(100).circle(80,mode='s').finalize().extrude(-20).union(w0.sketch().circle(80).circle(40,mode='s').push([(64,29)]).circle(15,mode='s').finalize().extrude(100)).union(w1.sketch().push([(0,-35)]).circle(29).push([(0,-35.5)]).rect(32,15,mode='s').finalize().extrude(-63))