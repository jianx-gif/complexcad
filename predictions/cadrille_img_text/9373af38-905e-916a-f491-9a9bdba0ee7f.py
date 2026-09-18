import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-97,0))
w1=cq.Workplane('ZX',origin=(0,-44,0))
r=w0.sketch().arc((-59,-46),(-56,-47),(-54,-50)).arc((56,49),(-59,-46)).assemble().finalize().extrude(194).union(w1.sketch().arc((-100,-40),(-74,-39),(-51,-50)).arc((-26,46),(5,-49)).arc((45,-59),(79,-78)).segment((79,78)).segment((-79,78)).segment((-79,50)).arc((-98,9),(-100,-40)).assemble().finalize().extrude(-56))