import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-25,0))
w1=cq.Workplane('ZX',origin=(0,-86,0))
r=w0.sketch().circle(100).circle(64,mode='s').finalize().extrude(51).union(w1.sketch().arc((-100,1),(-96,3),(-92,5)).arc((89,-19),(-89,19)).arc((-93,21),(-97,23)).arc((98,-21),(-100,1)).assemble().finalize().extrude(172))