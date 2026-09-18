import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,98))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().arc((-76,59),(58,48),(53,-78)).arc((66,-67),(76,-54)).segment((76,-59)).arc((87,0),(76,59)).segment((76,54)).arc((0,87),(-76,54)).close().assemble().finalize().extrude(-159).union(w1.sketch().arc((45,61),(-58,-29),(76,10)).arc((43,27),(45,61)).assemble().finalize().extrude(-200))