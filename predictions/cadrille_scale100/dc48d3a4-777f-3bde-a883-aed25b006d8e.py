import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,41))
w1=cq.Workplane('XY',origin=(0,0,57))
r=w0.workplane(offset=-71/2).cylinder(71,3).union(w0.sketch().circle(36).circle(24,mode='s').finalize().extrude(16)).union(w0.sketch().circle(14).push([(0,10)]).circle(2,mode='s').finalize().extrude(29)).union(w1.sketch().arc((-29,7),(-23,-20),(3,-30)).arc((5,-26),(8,-29)).arc((22,-20),(29,-7)).segment((23,-7)).arc((22,0),(23,7)).segment((29,7)).arc((28,11),(26,15)).arc((1,23),(-23,18)).arc((-23,15),(-26,15)).arc((-28,11),(-29,7)).assemble().finalize().extrude(-57))