import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-6))
r=w0.sketch().segment((-48,-4),(-45,-4)).segment((-45,-15)).arc((-21,-43),(16,-46)).segment((5,-46)).segment((5,-44)).segment((18,-44)).arc((33,-35),(43,-21)).segment((41,-21)).segment((41,-17)).segment((45,-17)).arc((48,5),(40,25)).segment((40,28)).segment((37,29)).arc((5,48),(-29,38)).segment((-32,39)).segment((-33,35)).arc((-45,17),(-48,-4)).assemble().push([(0,0)]).circle(15,mode='s').finalize().extrude(12).union(w0.sketch().segment((18,-1),(24,-5)).segment((28,1)).segment((22,5)).close().assemble().finalize().extrude(17))
