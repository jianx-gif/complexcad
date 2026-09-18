import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().arc((22,-33),(23,-32),(25,-31)).segment((22,-31)).close().assemble().finalize().extrude(-70).union(w0.sketch().circle(40).circle(35,mode='s').finalize().extrude(70))