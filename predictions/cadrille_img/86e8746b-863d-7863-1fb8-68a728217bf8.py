import cadquery as cq
w0=cq.Workplane('YZ',origin=(-1,0,0))
w1=cq.Workplane('XY',origin=(0,0,-73))
r=w0.sketch().segment((-100,-40),(-97,-40)).arc((0,-99),(97,-40)).segment((100,-40)).segment((100,-29)).arc((99,0),(100,29)).segment((100,40)).segment((97,40)).arc((0,99),(-97,40)).segment((-100,40)).segment((-100,29)).arc((-99,0),(-100,-29)).close().assemble().circle(99,mode='s').finalize().extrude(-69).union(w1.sketch().circle(100).push([(29,0)]).circle(43,mode='s').finalize().extrude(173))