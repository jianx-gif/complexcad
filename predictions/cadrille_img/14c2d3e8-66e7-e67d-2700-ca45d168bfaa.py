import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,59,0))
w1=cq.Workplane('YZ',origin=(86,0,0))
r=w0.sketch().push([(0,34)]).rect(120,106).circle(45,mode='s').circle(12).finalize().extrude(-119).union(w0.sketch().push([(0,34)]).rect(120,106).push([(0,33)]).circle(17,mode='s').push([(69,-39)]).circle(10).finalize().extrude(-115)).union(w1.sketch().arc((-87,-39),(1,-71),(87,-39)).segment((86,-39)).arc((87,0),(86,39)).segment((87,39)).arc((1,71),(-87,39)).segment((-86,39)).arc((-87,0),(-86,-39)).close().assemble().push([(59,11)]).circle(13,mode='s').finalize().extrude(-186))