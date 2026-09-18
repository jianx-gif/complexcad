import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,10))
w1=cq.Workplane('YZ',origin=(52,0,0))
r=w0.sketch().segment((-35,-22),(41,-22)).segment((41,1)).arc((47,1),(41,2)).segment((41,23)).segment((-35,23)).close().assemble().push([(-19,-4)]).circle(10,mode='s').push([(10,1)]).circle(4,mode='s').finalize().extrude(-11).union(w0.workplane(offset=-10/2).moveTo(10,1).cylinder(10,2)).union(w1.sketch().push([(0,0)]).rect(46,6).push([(-10,-0.5)]).rect(2,3,mode='s').finalize().extrude(-45))
