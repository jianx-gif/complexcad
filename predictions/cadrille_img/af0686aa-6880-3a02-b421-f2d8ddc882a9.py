import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-59,0))
w1=cq.Workplane('YZ',origin=(-33,0,0))
r=w0.sketch().push([(11,10)]).circle(89).push([(19,38)]).circle(45,mode='s').finalize().extrude(10).union(w0.sketch().arc((-1,-78),(18,-72),(36,-64)).arc((55,-49),(71,-30)).arc((78,-22),(84,-13)).arc((-49,79),(-1,-78)).assemble().finalize().extrude(134)).union(w1.sketch().push([(-11,11)]).circle(89).circle(49,mode='s').finalize().extrude(133))