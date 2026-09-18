import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-58,0))
r=w0.sketch().arc((-100,-45),(-14,-1),(79,-29)).arc((89,-29),(100,-30)).arc((1,69),(-100,-45)).assemble().finalize().extrude(155).union(w0.sketch().arc((-100,1),(-45,-45),(23,-69)).segment((23,-67)).arc((-44,-44),(-100,1)).assemble().finalize().extrude(156))