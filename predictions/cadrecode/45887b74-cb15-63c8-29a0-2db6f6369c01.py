import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-15))
r=w0.sketch().segment((-100,-75),(100,-75)).segment((100,-50)).segment((-75,-50)).segment((-75,75)).segment((-80,41)).segment((-80,40)).segment((-95,-50)).segment((-96,-50)).segment((-96,-51)).segment((-100,-74)).close().assemble().push([(-83,-62.5)]).rect(16,9,mode='s').push([(-81,-10)]).circle(3,mode='s').finalize().extrude(30)