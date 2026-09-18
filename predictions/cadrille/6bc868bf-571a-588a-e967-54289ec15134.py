import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,99))
r=w0.sketch().arc((-74,-57),(11,-91),(89,-34)).segment((96,-33)).segment((91,-10)).arc((92,2),(91,13)).segment((91,40)).segment((83,40)).arc((-56,83),(-74,-57)).assemble().finalize().extrude(-198).union(w0.sketch().circle(100).circle(94,mode='s').finalize().extrude(-112))