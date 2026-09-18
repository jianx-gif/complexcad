import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,4))
r=w0.sketch().segment((-50,-40),(50,-40)).segment((50,40)).segment((14,40)).segment((14,30)).segment((33,30)).segment((33,22)).segment((14,22)).segment((14,-13)).segment((4,-13)).segment((4,22)).segment((-16,22)).segment((-16,30)).segment((4,30)).segment((4,40)).segment((-50,40)).close().assemble().finalize().extrude(-4).union(w0.sketch().rect(28,78).circle(12,mode='s').finalize().extrude(-3))
