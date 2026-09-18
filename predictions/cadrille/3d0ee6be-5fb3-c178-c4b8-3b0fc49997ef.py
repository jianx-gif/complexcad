import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,68))
r=w0.sketch().circle(68).circle(9,mode='s').finalize().extrude(-153).union(w0.sketch().circle(87).circle(9,mode='s').finalize().extrude(-143)).union(w0.sketch().arc((-98,-22),(-90,-30),(-90,-41)).arc((95,29),(-98,-22)).assemble().push([(0,-1)]).rect(34,86,mode='s').finalize().extrude(17))