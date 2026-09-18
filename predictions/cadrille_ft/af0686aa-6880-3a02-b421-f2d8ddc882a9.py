import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-48,0))
w1=cq.Workplane('XY',origin=(0,0,45))
r=w0.sketch().segment((-57,2),(-55,2)).segment((-55,-20)).arc((57,20),(-57,2)).assemble().finalize().extrude(-21).union(w0.sketch().arc((-24,-48),(18,-88),(54,-44)).arc((10,88),(-24,-48)).assemble().push([(16,10)]).circle(38,mode='s').finalize().extrude(125)).union(w1.sketch().arc((-88,47),(78,-60),(-50,86)).arc((-70,68),(-88,47)).assemble().finalize().extrude(-56))