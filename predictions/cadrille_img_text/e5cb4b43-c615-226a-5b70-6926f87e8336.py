import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,68))
w1=cq.Workplane('YZ',origin=(59,0,0))
r=w0.sketch().push([(-1,0)]).rect(198,120).circle(88,mode='s').circle(58).finalize().extrude(-119).union(w1.sketch().push([(0,1)]).circle(90).circle(65,mode='s').push([(54,34)]).circle(13,mode='s').finalize().extrude(-67))