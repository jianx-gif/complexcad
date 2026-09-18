import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-69,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().push([(18,36)]).circle(27).circle(24,mode='s').finalize().extrude(139).union(w0.sketch().segment((-99,1),(-98,0)).segment((99,-34)).segment((99,-23)).close().assemble().finalize().extrude(163)).union(w1.sketch().segment((-84,-71),(-57,-71)).arc((0,-87),(57,-71)).segment((84,-71)).segment((84,-28)).arc((87,-10),(84,8)).segment((84,51)).segment((57,51)).arc((0,67),(-57,51)).segment((-84,51)).segment((-84,8)).arc((-87,-10),(-84,-28)).close().assemble().finalize().extrude(-200))