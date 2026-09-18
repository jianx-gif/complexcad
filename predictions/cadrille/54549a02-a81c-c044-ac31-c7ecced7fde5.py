import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-1))
w1=cq.Workplane('XY',origin=(0,0,-8))
r=w0.sketch().rect(200,108).push([(40,-13)]).rect(84,80,mode='s').finalize().extrude(-14).union(w1.sketch().segment((-100,-54),(64,-54)).segment((64,-3)).segment((89,-3)).segment((89,18)).segment((64,18)).segment((64,49)).segment((59,49)).segment((59,54)).segment((56,54)).segment((56,49)).segment((-100,49)).close().assemble().push([(-19,-31)]).rect(90,28,mode='s').push([(-19,0)]).rect(90,18,mode='s').finalize().extrude(23))