import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-97,0))
w1=cq.Workplane('ZX',origin=(0,-60,0))
r=w0.sketch().circle(81).circle(73,mode='s').finalize().extrude(194).union(w1.sketch().segment((-100,-48),(-97,-48)).arc((-39,-95),(33,-95)).arc((35,-87),(41,-89)).arc((72,-65),(91,-30)).segment((91,-29)).arc((92,-22),(93,-15)).segment((93,-14)).segment((93,-13)).arc((89,28),(68,64)).segment((68,65)).segment((67,65)).arc((0,89),(-67,65)).segment((-68,65)).segment((-68,64)).arc((-89,29),(-97,-10)).segment((-100,-10)).close().assemble().finalize().extrude(120))