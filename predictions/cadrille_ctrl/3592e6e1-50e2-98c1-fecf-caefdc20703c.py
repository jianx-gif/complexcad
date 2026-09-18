import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,4))
w1=cq.Workplane('XY',origin=(0,0,13))
r=w0.sketch().rect(100,30).push([(39,1)]).circle(5,mode='s').finalize().extrude(-8).union(w0.sketch().segment((-50,-8),(49,-15)).segment((50,8)).segment((-49,15)).close().assemble().circle(10,mode='s').finalize().extrude(-2)).union(w1.sketch().segment((-45,-6),(-45,-2)).segment((-39,-2)).segment((-39,-10)).segment((-41,-10)).arc((-37,-14),(-32,-16)).segment((-32,-1)).segment((-2,-1)).segment((-2,-16)).arc((3,-14),(8,-10)).segment((4,-10)).segment((4,-6)).segment((10,-6)).segment((10,-9)).arc((12,-7),(13,-6)).segment((45,-6)).segment((45,6)).segment((13,6)).arc((0,15),(-13,6)).segment((-45,6)).segment((-45,3)).segment((-40,3)).segment((-40,-6)).close().assemble().finalize().extrude(-16))
