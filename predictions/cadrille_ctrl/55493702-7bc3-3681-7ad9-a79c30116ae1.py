import cadquery as cq
w0=cq.Workplane('YZ',origin=(40,0,0))
w1=cq.Workplane('XY',origin=(0,0,8))
r=w0.sketch().push([(0,10)]).rect(50,20).rect(46,16,mode='s').finalize().extrude(-80).union(w0.sketch().segment((-7,23),(7,23)).arc((0,24),(-7,23)).assemble().finalize().extrude(2)).union(w1.sketch().segment((-100,-15),(-40,-15)).segment((-40,-14)).segment((-38,-14)).segment((-38,-15)).segment((-32,-15)).segment((-32,15)).segment((-100,15)).close().assemble().finalize().extrude(12))
