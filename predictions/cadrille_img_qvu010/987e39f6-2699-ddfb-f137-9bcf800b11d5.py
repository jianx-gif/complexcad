import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,11,0))
w1=cq.Workplane('ZX',origin=(0,38,0))
r=w0.sketch().circle(100).circle(96,mode='s').circle(22).circle(13,mode='s').push([(-47,-66)]).circle(10).push([(47,-66)]).circle(10).finalize().extrude(-18).union(w1.sketch().segment((-21,-72),(21,-72)).segment((21,-58)).arc((60,-51),(88,-23)).arc((91,-19),(93,-14)).arc((95,-10),(96,-6)).arc((-79,-61),(21,98)).segment((21,72)).segment((-21,72)).segment((-21,58)).arc((-60,0),(-21,-58)).close().assemble().finalize().extrude(-76))