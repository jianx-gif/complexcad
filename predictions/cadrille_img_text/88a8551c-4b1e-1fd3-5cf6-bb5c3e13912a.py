import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-1,0))
w1=cq.Workplane('YZ',origin=(73,0,0))
r=w0.sketch().segment((-91,93),(-82,-39)).segment((91,-27)).segment((82,100)).close().assemble().push([(0,30)]).circle(53,mode='s').circle(14).finalize().extrude(-25).union(w1.sketch().arc((-81,-34),(-59,-37),(-38,-43)).arc((-38,-31),(-35,-19)).segment((-35,-13)).segment((-32,-13)).arc((0,13),(32,-13)).segment((35,-13)).segment((35,-19)).arc((38,-30),(37,-41)).arc((59,-40),(81,-34)).arc((0,100),(-81,-34)).assemble().finalize().extrude(-101))