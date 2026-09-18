import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-60,0))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().arc((-26,22),(-17,24),(-8,25)).arc((-1,51),(16,73)).arc((-10,54),(-26,26)).close().assemble().finalize().extrude(125).union(w1.sketch().segment((-89,-53),(-58,-53)).arc((-57,-55),(-55,-57)).segment((-55,-53)).segment((55,-53)).segment((55,-57)).arc((57,-55),(58,-53)).segment((89,-53)).segment((89,-22)).arc((0,-89),(-89,-22)).close().assemble().finalize().extrude(200))