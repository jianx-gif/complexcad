import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,33))
w1=cq.Workplane('YZ',origin=(76,0,0))
r=w0.sketch().circle(83).circle(33,mode='s').finalize().extrude(-66).union(w0.sketch().circle(100).circle(34,mode='s').finalize().extrude(-54)).union(w1.sketch().push([(0,-1)]).circle(33).push([(0,-0.5)]).rect(30,19,mode='s').finalize().extrude(-167))