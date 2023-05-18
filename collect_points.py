import xlsxwriter
import triad_openvr
import time
import sys

FILE_NAME = 'trackerdata.xlsx'

wb = xlsxwriter.Workbook(FILE_NAME)
ws = wb.add_worksheet()

v = triad_openvr.triad_openvr()
v.print_discovered_objects()

rn = 0          # row num start
maxrn = 2500

if len(sys.argv) == 1:
    interval = 1/250
elif len(sys.argv) == 2:
    interval = 1/float(sys.argv[1])
else:
    print("Invalid number of arguments")
    interval = False
if interval:
    while(True):
        if rn > maxrn: break
        start = time.time()
        txt = ""
        for each in v.devices["tracker_1"].get_pose_euler():
            txt += "%.4f" % each
            txt += " "
        data = txt.split()
        for cn,d in enumerate(data):
            ws.write(rn, cn, d)
        rn+=1    
        print("\r" + txt + " " + str(rn), end="")
        sleep_time = interval-(time.time()-start)
        if sleep_time>0:
            time.sleep(sleep_time)

wb.close()
