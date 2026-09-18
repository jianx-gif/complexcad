import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-19,-19))
w1=cq.Workplane('XY',origin=(-100,-19,-19))
r=w0.sketch().circle(5).circle(4,mode='s').finalize().extrude(39).union(w1.sketch().segment((92,-19),(92,-16)).segment((95,-16)).arc((98,-14),(100,-14)).arc((98,-13),(97,-11)).segment((97,-11)).segment((97,-8)).segment((97,-7)).segment((97,-4)).segment((97,-1)).segment((97,1)).segment((97,4)).segment((97,7)).segment((97,10)).arc((98,11),(98,12)).arc((98,15),(100,19)).arc((-100,1),(99,-19)).close().assemble().finalize().extrude(39))