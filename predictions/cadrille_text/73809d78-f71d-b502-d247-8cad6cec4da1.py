import cadquery as cq
w0=cq.Workplane('ZX',origin=(-100,100,0))
w1=cq.Workplane('ZX',origin=(-100,100,0))
r=w0.sketch().segment((52,-59),(59,-59)).segment((59,-54)).arc((56,-56),(52,-59)).assemble().finalize().extrude(-200).union(w1.sketch().face(w1.sketch().segment((0,0),(0,200)).arc((-53,40),(0,0)).assemble()).finalize().extrude(-110))