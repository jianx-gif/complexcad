import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,11,0))
w1=cq.Workplane('ZX',origin=(0,16,0))
r=w0.sketch().segment((-90,17),(-86,-25)).segment((-52,-22)).segment((-52,16)).segment((-22,16)).segment((-22,-20)).segment((90,-10)).segment((86,42)).close().assemble().finalize().extrude(-23).union(w1.sketch().arc((35,-77),(59,-87),(85,-89)).arc((86,-95),(90,-100)).segment((90,100)).arc((86,95),(83,90)).arc((15,12),(35,-77)).assemble().push([(51,0)]).circle(25,mode='s').finalize().extrude(-32))