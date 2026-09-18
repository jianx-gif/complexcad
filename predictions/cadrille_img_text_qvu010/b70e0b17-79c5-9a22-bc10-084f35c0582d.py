import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
w1=cq.Workplane('ZX',origin=(0,87,0))
r=w0.sketch().arc((-95,10),(-49,-10),(-10,-43)).arc((16,-46),(39,-58)).arc((66,-43),(88,-22)).arc((87,-17),(91,-15)).arc((93,-12),(95,-10)).segment((89,-10)).arc((73,-24),(54,-32)).arc((47,-36),(40,-32)).arc((-21,10),(-19,84)).arc((-62,61),(-88,15)).arc((-92,13),(-95,10)).assemble().finalize().extrude(-192).union(w1.sketch().push([(0,1)]).circle(68).circle(33,mode='s').finalize().extrude(-143))