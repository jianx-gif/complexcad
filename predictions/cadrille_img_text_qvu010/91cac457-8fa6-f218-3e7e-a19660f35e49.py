import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,11,0))
w1=cq.Workplane('ZX',origin=(0,75,0))
r=w0.sketch().arc((-91,56),(-54,-68),(72,-73)).segment((89,-90)).segment((89,-56)).arc((96,-37),(99,-17)).segment((91,-25)).arc((54,68),(-52,73)).segment((-89,90)).segment((-89,56)).close().assemble().circle(63,mode='s').finalize().extrude(-21).union(w1.sketch().arc((-54,59),(-14,29),(1,-18)).arc((27,-39),(49,-66)).arc((56,-57),(62,-47)).arc((15,10),(-54,59)).assemble().finalize().extrude(-150))