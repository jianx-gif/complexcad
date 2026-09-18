import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-40,-29),(-38,-29)).segment((-38,-30)).segment((38,-30)).segment((38,-29)).segment((40,-29)).segment((40,29)).segment((38,29)).segment((38,30)).segment((-38,30)).segment((-38,29)).segment((-40,29)).close().assemble().push([(0,-5.5)]).rect(74,39,mode='s').finalize().extrude(-100)
