import cv2
import numpy as np
import twophase.solver as Cube
state=  {
            'up':['white','white','white','white','blue','white','white','white','white',],
            'right':['white','white','white','white','blue','white','white','white','white',],
            'front':['white','white','white','white','blue','white','white','white','white',],
            'down':['white','white','white','white','blue','white','white','white','white',],
            'left':['white','white','white','white','blue','white','white','white','white',],
            'back':['white','white','white','white','blue','white','white','white','white',]
        }

sign_conv={
            'green'  : 'R',
            'white'  : 'D',
            'blue'   : 'L',
            'red'    : 'F',
            'orange' : 'B',
            'yellow' : 'U'
          }

color = {
        'red'    : (0,0,255),
        'orange' : (0,165,255),
        'blue'   : (255,0,0),
        'green'  : (0,255,0),
        'white'  : (255,255,255),
        'yellow' : (0,255,255)
        }

stickers = {
        'main': [
            [200, 120], [300, 120], [400, 120],
            [200, 220], [300, 220], [400, 220],
            [200, 320], [300, 320], [400, 320]
        ],
        'current': [
            [20, 20], [54, 20], [88, 20],
            [20, 54], [54, 54], [88, 54],
            [20, 88], [54, 88], [88, 88]
        ],
        'preview': [
            [20, 130], [54, 130], [88, 130],
            [20, 164], [54, 164], [88, 164],
            [20, 198], [54, 198], [88, 198]
        ],
        'left': [
            [50, 280], [94, 280], [138, 280],
            [50, 324], [94, 324], [138, 324],
            [50, 368], [94, 368], [138, 368]
        ],
        'front': [
            [188, 280], [232, 280], [276, 280],
            [188, 324], [232, 324], [276, 324],
            [188, 368], [232, 368], [276, 368]
        ],
        'right': [
            [326, 280], [370, 280], [414, 280],
            [326, 324], [370, 324], [414, 324],
            [326, 368], [370, 368], [414, 368]
        ],
        'up': [
            [188, 128], [232, 128], [276, 128],
            [188, 172], [232, 172], [276, 172],
            [188, 216], [232, 216], [276, 216]
        ],
        'down': [
            [188, 434], [232, 434], [276, 434],
            [188, 478], [232, 478], [276, 478],
            [188, 522], [232, 522], [276, 522]
        ],
        'back': [
            [464, 280], [508, 280], [552, 280],
            [464, 324], [508, 324], [552, 324],
            [464, 368], [508, 368], [552, 368]
        ],
           }

check_state=[]
solution=[]
solved=False

cap=cv2.VideoCapture(0)
cv2.namedWindow('frame')
def solve(state):
    raw=''
    for i in state:
        for j in state[i]:
            raw+=sign_conv[j]
    st = Cube.solve(raw)

    ### This part is used to eleminate the show the output to the suitable form
    store = ''
    ii = 0
    length = len(st)
    if st[length-1] == ')':
        if st[length-4] == '(':       # because the god number is 20 .....(20f)
            length-=5
            for ii in range(length):
                store += st[ii]
        else:
            length-=6
            for ii in range(length):
                store += st[ii]
    print("answer:",store)
    import serial
    import time
    ser=serial.Serial('COM5',9600)
    ser.timeout=1
    counter=1
    while True: 
        transfer=store.strip()
        ser.write(transfer.encode())
        time.sleep(0.5)
        if counter>2:
            break
        print(counter)
        print(store)
        counter+=1
    ser.close()

    ### this part is used to convert the output to the letter representation
    temp = []
    cnt = 0
    for cnt in range(len(store)):
        if store[cnt]=='L':
            if int(store[cnt+1])==1:
                temp.append('A')
            elif int(store[cnt + 1]) ==2:
                    temp.append('B')
            elif int(store[cnt + 1]) ==3:
                    temp.append('C')
        if store[cnt] == 'R':
            if int(store[cnt + 1]) == 1:
                temp.append('D')
            elif int(store[cnt + 1]) == 2:
                temp.append('E')
            elif int(store[cnt + 1]) == 3:
                temp.append('F')
        if store[cnt]=='U':
            if int(store[cnt+1])==1:
                temp.append('G')
            elif int(store[cnt + 1]) ==2:
                    temp.append('H')
            elif int(store[cnt + 1]) ==3:
                    temp.append('I')
        if store[cnt]=='D':
            if int(store[cnt+1])==1:
                temp.append('J')
            elif int(store[cnt + 1]) ==2:
                    temp.append('K')
            elif int(store[cnt + 1]) ==3:
                    temp.append('L')
        if store[cnt]=='B':
            if int(store[cnt+1])==1:
                temp.append('M')
            elif int(store[cnt + 1]) ==2:
                    temp.append('N')
            elif int(store[cnt + 1]) ==3:
                    temp.append('O')
        cnt+=3
    print(temp)
    return Cube.solve(raw)

def color_detect(h,s,v):
    # print(h,s,v)
    if h < 2 and s >= 69 and v >= 33 and v <= 152:
        return 'red'
    elif h < 15 and h >= 0 and s >= 172 and v >= 108:
        return 'orange'
    elif h >= 25 and h <=47  and s > 218 and v >=51 and v<=125:
        return 'yellow'
    elif h >= 49 and h <= 80 and s > 194 and v > 37 and v < 255:
        return 'green'
   
    elif h <= 100 and s < 10 and v < 200:
        return 'white'
    return 'white'

def draw_stickers(frame,stickers,name):
        for x,y in stickers[name]:
            cv2.rectangle(frame, (x,y), (x+30, y+30), (255,255,255), 2)


def draw_preview_stickers(frame,stickers):
        stick=['front','back','left','right','up','down']
        for name in stick:
            for x,y in stickers[name]:
                cv2.rectangle(frame, (x,y), (x+40, y+40), (255,255,255), 2)

def fill_stickers(frame,stickers,sides):
    for side,colors in sides.items():
        num=0
        for x,y in stickers[side]:
            cv2.rectangle(frame,(x,y),(x+40,y+40),color[colors[num]],-1)
            num+=1

if __name__=='__main__':

    preview = np.zeros((700,800,3), np.uint8)

    while True:
        hsv=[]
        current_state=[]
        ret,img=cap.read()
        # img=cv2.flip(img,1)
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = np.zeros(frame.shape, dtype=np.uint8)

        draw_stickers(img,stickers,'main')
        draw_stickers(img,stickers,'current')
        draw_preview_stickers(preview,stickers)
        fill_stickers(preview,stickers,state)

        for i in range(9):
            hsv.append(frame[stickers['main'][i][1]+10][stickers['main'][i][0]+10])

        a=0
        for x,y in stickers['current']:
            color_name=color_detect(hsv[a][0],hsv[a][1],hsv[a][2])
            cv2.rectangle(img,(x,y),(x+30,y+30),color[color_name],-1)
            a+=1
            current_state.append(color_name)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
        elif k ==ord('u'):
            state['up']=current_state
            check_state.append('u')
        elif k ==ord('r'):
            check_state.append('r')
            state['right']=current_state
        elif k ==ord('l'):
            check_state.append('l')
            state['left']=current_state
        elif k ==ord('d'):
            check_state.append('d')
            state['down']=current_state
        elif k ==ord('f'):
            check_state.append('f')
            state['front']=current_state
        elif k ==ord('b'):
            check_state.append('b')
            state['back']=current_state
        elif k == ord('\r'):
            # process(["R","R'"])
            if len(set(check_state))==6:
                try:
                    solved=solve(state)
                except:
                    print("error in side detection ,you may do not follow sequence or some color not detected well.Try again")
            else:
                print("all side are not scanned check other window for finding which left to be scanned?")
                print("left to scan:",6-len(set(check_state)))
        cv2.imshow('preview',preview)
        cv2.imshow('frame',img[0:500,0:500])
    cv2.destroyAllWindows()

