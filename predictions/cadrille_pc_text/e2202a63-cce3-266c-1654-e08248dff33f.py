import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
w1=cq.Workplane('XY',origin=(0,0,-14))
r=w0.sketch().arc((-57,10),(-57,-10),(-49,-29)).segment((-49,-30)).segment((-48,-30)).arc((0,-57),(48,-30)).segment((49,-30)).segment((49,-29)).arc((57,0),(49,29)).segment((49,30)).segment((48,30)).arc((0,57),(-48,30)).segment((-49,30)).segment((-49,29)).arc((-54,20),(-57,10)).assemble().circle(7,mode='s').finalize().extrude(-86).union(w0.sketch().circle(86).circle(62,mode='s').finalize().extrude(-14)).union(w1.sketch().circle(86).circle(51,mode='s').finalize().extrude(-86))