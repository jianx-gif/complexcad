import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,94,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-86,-12),(-82,-21)).segment((86,12)).segment((82,21)).close().assemble().finalize().extrude(-100).union(w1.sketch().segment((-96,-24),(-76,-24)).segment((-76,-30)).segment((76,-30)).segment((76,-24)).segment((96,-24)).segment((96,24)).segment((76,24)).segment((76,30)).segment((-76,30)).segment((-76,24)).segment((-96,24)).close().assemble().finalize().extrude(-200))