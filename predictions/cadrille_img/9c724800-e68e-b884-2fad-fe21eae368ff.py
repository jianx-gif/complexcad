import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-14,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().push([(0,19)]).circle(71).push([(-54,1)]).circle(13,mode='s').push([(82,-11)]).circle(12,mode='s').finalize().extrude(14).union(w1.sketch().arc((-96,-55),(-19,-36),(50,-71)).arc((63,-61),(74,-50)).arc((1,-30),(-33,38)).arc((-39,51),(-39,65)).arc((-42,70),(-44,76)).arc((-90,23),(-96,-55)).assemble().finalize().extrude(-200))