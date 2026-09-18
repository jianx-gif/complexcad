import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
w1=cq.Workplane('YZ',origin=(21,0,0))
r=w0.sketch().segment((-21,-34),(19,-34)).segment((19,-29)).arc((34,-10),(33,13)).arc((25,1),(13,-7)).segment((13,-10)).segment((10,-10)).segment((10,-7)).arc((-5,1),(1,17)).arc((-1,26),(1,34)).segment((-21,34)).segment((-21,29)).arc((-39,0),(-21,-29)).close().assemble().finalize().extrude(-100).union(w0.sketch().push([(0,-0.5)]).rect(40,69).push([(0,0)]).circle(5,mode='s').finalize().extrude(-92)).union(w1.workplane(offset=22/2).moveTo(-1.5,98.5).box(59,3,22))