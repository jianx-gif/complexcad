import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-40,-29),(-38,-29)).segment((-38,-30)).segment((38,-30)).segment((38,-29)).segment((40,-29)).segment((40,29)).segment((38,29)).segment((38,30)).segment((-38,30)).segment((-38,29)).segment((-40,29)).close().assemble().rect(76,50,mode='s').finalize().extrude(-100)