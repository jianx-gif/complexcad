import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-57,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().arc((-68,-63),(17,35),(74,-80)).arc((89,-72),(100,-63)).segment((100,34)).segment((100,35)).segment((100,36)).segment((99,36)).arc((87,49),(72,59)).segment((72,63)).segment((65,63)).arc((0,85),(-65,63)).segment((-68,63)).segment((-68,59)).arc((-94,-2),(-68,-63)).assemble().finalize().extrude(154).union(w1.sketch().arc((-85,-99),(1,-78),(85,-99)).segment((85,-1)).segment((-85,-1)).close().assemble().push([(39,-40)]).circle(18,mode='s').finalize().extrude(-161))