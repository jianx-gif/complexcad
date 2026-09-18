import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-1,0))
w1=cq.Workplane('ZX',origin=(0,-29,0))
r=w0.sketch().segment((-33,-67),(-33,-66)).segment((-29,-66)).segment((-29,-70)).arc((31,71),(-33,-67)).assemble().finalize().extrude(11).union(w1.sketch().push([(13,14)]).circle(87).reset().face(w1.sketch().segment((-26,-51),(-19,-51)).arc((13,-58),(44,-51)).segment((51,-51)).segment((51,-47)).arc((89,14),(51,74)).segment((51,78)).segment((44,78)).arc((13,85),(-19,78)).segment((-26,78)).segment((-26,74)).arc((-54,14),(-26,-47)).close().assemble(),mode='s').finalize().extrude(58))