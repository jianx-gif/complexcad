import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-12))
r=w0.sketch().segment((-100,-85),(-64,-85)).segment((-64,-61)).segment((100,-61)).segment((100,-36)).segment((-64,-36)).segment((-64,-12)).segment((-70,-12)).segment((-70,85)).segment((-94,85)).segment((-94,-12)).segment((-100,-12)).close().assemble().push([(3,-48)]).circle(10,mode='s').finalize().extrude(24)