import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-18))
r=w0.sketch().segment((-100,-12),(-57,-22)).arc((16,0),(98,-34)).segment((100,-31)).segment((100,6)).segment((98,6)).segment((98,8)).segment((96,8)).segment((98,10)).segment((25,34)).arc((-1,33),(-26,30)).segment((-33,28)).segment((-34,28)).close().assemble().finalize().extrude(36)