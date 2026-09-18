import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,41))
w1=cq.Workplane('XY',origin=(0,0,57))
r=w0.workplane(offset=-72/2).cylinder(72,3).union(w0.sketch().circle(36).circle(23,mode='s').finalize().extrude(16)).union(w0.sketch().circle(14).push([(0,10)]).circle(2,mode='s').finalize().extrude(29)).union(w1.sketch().arc((-29,8),(-23,-20),(3,-30)).arc((5,-26),(8,-29)).arc((21,-21),(29,-8)).segment((23,-8)).arc((24,0),(23,8)).segment((29,8)).arc((0,30),(-29,8)).assemble().finalize().extrude(-57))
