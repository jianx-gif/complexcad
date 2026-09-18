import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,39,0))
r=w0.sketch().segment((-71,-57),(-67,-57)).arc((13,-89),(92,-57)).segment((96,-57)).segment((96,-51)).arc((100,-44),(100,-36)).arc((-79,61),(71,-71)).arc((68,-66),(67,-61)).arc((-73,60),(96,-23)).segment((96,23)).segment((92,23)).arc((13,65),(-67,23)).segment((-71,23)).close().assemble().finalize().extrude(-78)