import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
w1=cq.Workplane('ZX',origin=(0,59,0))
r=w0.sketch().push([(-29,-27)]).circle(48).circle(47,mode='s').finalize().extrude(-200).union(w0.sketch().arc((-96,-30),(-29,-95),(48,-43)).arc((95,31),(29,95)).segment((29,89)).arc((93,31),(49,-43)).arc((-29,43),(-95,-42)).arc((-97,-36),(-96,-30)).assemble().finalize().extrude(-121)).union(w1.sketch().arc((-49,43),(-78,-73),(37,-46)).arc((77,66),(-40,54)).segment((-40,43)).close().assemble().push([(-29,-27)]).circle(59,mode='s').finalize().extrude(-149))