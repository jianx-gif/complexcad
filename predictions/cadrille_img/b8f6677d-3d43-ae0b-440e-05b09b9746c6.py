import cadquery as cq
w0=cq.Workplane('YZ',origin=(-100,0,0))
w1=cq.Workplane('ZX',origin=(0,-29,0))
r=w0.sketch().arc((-95,-32),(-72,-35),(-49,-36)).segment((-49,-93)).segment((78,-87)).segment((78,-49)).arc((88,-39),(95,-27)).segment((-14,-32)).segment((-14,-33)).segment((-18,-33)).segment((-18,-32)).close().assemble().push([(50,-60)]).circle(7,mode='s').push([(50,39)]).rect(10,100).push([(50,38)]).circle(4,mode='s').finalize().extrude(200).union(w1.sketch().push([(30,43)]).circle(43).circle(35,mode='s').finalize().extrude(-26))