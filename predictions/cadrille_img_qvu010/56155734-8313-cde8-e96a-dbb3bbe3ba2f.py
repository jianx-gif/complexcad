import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-48,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().push([(84,-19)]).circle(16).circle(14,mode='s').finalize().extrude(11).union(w1.sketch().arc((-76,-53),(-12,-18),(43,-65)).arc((58,-49),(67,-30)).segment((67,-28)).segment((68,-28)).arc((70,-26),(71,-23)).segment((72,-23)).segment((72,-21)).arc((74,0),(72,21)).segment((72,23)).segment((71,23)).arc((59,57),(32,83)).segment((32,79)).segment((28,79)).segment((28,84)).arc((-74,56),(-76,-53)).assemble().push([(-12,0)]).circle(33,mode='s').finalize().extrude(-200))