import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,47))
w1=cq.Workplane('XY',origin=(0,0,25))
r=w0.sketch().push([(-30,0)]).circle(12).circle(3,mode='s').finalize().extrude(-100).union(w0.sketch().push([(-94,-87)]).rect(6,26).push([(-94.5,-75.5)]).rect(1,3,mode='s').finalize().extrude(6)).union(w1.sketch().segment((27,98),(97,98)).segment((97,100)).segment((91,100)).segment((91,99)).segment((88,99)).segment((88,100)).segment((27,100)).close().assemble().finalize().extrude(-73))