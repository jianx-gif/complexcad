import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,5))
r=w0.sketch().segment((-21,10),(-19,-1)).segment((-19,-19)).segment((-16,-19)).segment((-15,-26)).segment((21,-26)).segment((21,26)).segment((-21,26)).segment((-21,11)).segment((-19,11)).segment((-19,10)).close().assemble().finalize().extrude(-7).union(w0.sketch().rect(80,60).push([(11,11)]).circle(13,mode='s').finalize().extrude(-5))
