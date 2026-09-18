import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
w1=cq.Workplane('XY',origin=(0,0,-40))
r=w0.sketch().segment((-99,-44),(-86,-44)).segment((-86,-64)).arc((94,36),(-99,-44)).assemble().push([(10,11)]).circle(46,mode='s').finalize().extrude(-182).union(w0.sketch().segment((-98,-40),(-67,-40)).arc((-69,-50),(-67,-60)).segment((-84,-60)).arc((93,38),(-98,-40)).assemble().finalize().extrude(-73)).union(w1.sketch().push([(11,0)]).circle(99).circle(68,mode='s').finalize().extrude(131))