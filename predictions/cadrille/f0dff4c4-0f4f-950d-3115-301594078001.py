import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,20))
w1=cq.Workplane('XY',origin=(0,0,28))
r=w0.sketch().circle(100).circle(43,mode='s').push([(81,-1)]).rect(30,22,mode='s').finalize().extrude(-49).union(w1.sketch().arc((-84,-54),(-18,-39),(-21,-98)).arc((57,82),(-84,-54)).assemble().push([(1,1)]).circle(19,mode='s').finalize().extrude(-11))