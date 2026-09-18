import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
w1=cq.Workplane('ZX',origin=(0,86,0))
r=w0.sketch().segment((-90,-55),(-48,-55)).arc((-49,-51),(-50,-46)).segment((90,-52)).segment((90,-33)).segment((-90,-28)).close().assemble().reset().face(w0.sketch().segment((-90,33),(90,28)).segment((90,46)).segment((48,52)).arc((49,49),(50,44)).segment((-90,52)).close().assemble()).finalize().extrude(-200).union(w1.sketch().arc((-86,-63),(-79,-66),(-72,-68)).segment((-72,68)).arc((-80,66),(-86,63)).close().assemble().finalize().extrude(-48))