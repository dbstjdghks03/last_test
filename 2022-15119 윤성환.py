'''벌레를 잡아먹을 때마다 거북이 크기가 커짐'''
import turtle as t
import random
import math

screen = t.Screen()     #Screen 객체 통해 전체 화면을 제어하는 객체, 화면의 크기, 배경색, 키보드 입출력 이벤트를 관리
screen.bgcolor("lightgreen")
screen.tracer(2)        #스크린의 그래픽 그리는 속도를 높임

mypen = t.Turtle()              #울타리 객체 생성
mypen.penup()                   #붓을 올림(잉크 안 보임)
mypen.setposition(-300, 300)    #객체의 위치 이동
mypen.pendown()                 #붓을 내림(잉크 보임)
mypen.pensize(3)                #굵기 변경

for x in range(4):
    mypen.forward(600)
    mypen.right(90)
    #mypen.circle(5)

#mypen.hideturtle()              #turtle 객체가 안보이게 생성

maxBugs = 20                                                                #bug 개수 20마리
bugs = []                                                                   #생성된 bug 객체를 관리할 list
colors = ['red', 'blue', 'purple', 'white', 'black', 'pink']                #color 후보
shapes = ['arrow', 'blank', 'circle', 'classic', 'square', 'triangle']      #shape 후보

for b in range(maxBugs):
    c = random.randint(0, 5)                        #각 bug마다 랜덤 color 고름
    s = random.randint(0, 5)                        #각 bug마다 랜덤 shape 고름
    bugs.append(t.Turtle())                         #새로운 bug 객체를 bugs 리스트에 추가
    bugs[b].color(colors[c])
    bugs[b].shape(shapes[s])
    bugs[b].penup()
    bugs[b].speed(0)                                #애니메이션 효과 끔
    bugs[b].setposition(random.randint(-300, 300), random.randint(-300, 300))   #랜덤 위치 선정
    bugs[b].right(random.randint(0, 360))           #랜덤 초기 각도 선정

size = 1
p = t.Turtle()          #turtle 객체를 생성하여 p라는 instance를 생성
p.shape("turtle")       #거북이 모양
p.turtlesize(size, size)
p.color("blue")

speed = 1               #거북이의 움직임 속도 디폴트 값 1
score = 0

def turnleft():
    p.left(30)

def turnright():
    p.right(30)

def increasespeed():
    global speed
    speed += 1

def decreasespeed():
    global speed
    speed -= 1


def setScore(score):          #점수 작성 함수
    print(mypen.undobufferentries())
    mypen.undo()              #이전 행동 되돌림, 반복적으로 write 시 겹쳐 쓰는 것 방지
    mypen.penup()
    mypen.hideturtle()
    mypen.setposition(-290, 310)            #점수판 위치
    scorestring = "Score: {}".format(score) #점수 불러오기
    mypen.write(scorestring, False, align="left", font=("Arial", 14, "normal")) #점수 작성

def isCollision(t1, t2):      #충돌 확인 함수
    d = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    if d < 20:                 #두 점 사이 거리가 20 이하이면 충돌 true
        return True
    else:                      #아니면 false
        return False


screen.listen()                         #키보드 입력 대기
screen.onkey(turnleft, "Left")          #키보드 <- 키 눌렀다 떼면 turnleft 함수 발동
screen.onkey(turnright, "Right")        #키보드 -> 키 눌렀다 떼면 turnright 함수 발동
screen.onkey(increasespeed, "Up")
screen.onkey(decreasespeed, "Down")

while True:
    p.forward(speed)

    #거북이가 울타리를 벗어낫는지 체크
    if p.xcor() > 300 or p.xcor() < -300:       #거북이의 x좌표를 울타리와 비교
        p.right(180)

    if p.ycor() > 300 or p.ycor() < -300:       #거북이의 y좌표를 울타리와 비교
        p.right(180)

    #벌레의 움직임 생성
    for b in range(maxBugs):
        bugs[b].forward(5)                      #각 벌레는 속도 5로 움직임

        # 각 벌레가 울타리를 벗어낫는지 체크
        if bugs[b].xcor() > 300 or bugs[b].xcor() < -300:   #각 벌레의 x좌표를 울타리와 비교
            bugs[b].right(180)

        if bugs[b].ycor() > 300 or bugs[b].ycor() < -300:   #각 벌레의 y좌표를 울타리와 비교
            bugs[b].right(180)

        if isCollision(p, bugs[b]): # 두 점과의 거리가 0일때 일치, 서로간의 거리가 20정도 되면 먹은 것으로 생각
            # 벌레가 먹히면 색상, 모양, 움직임 각도 변경후 다른 곳으로 이동
            bugs[b].setposition(random.randint(-300, 300), random.randint(-300, 300))
            bugs[b].right(random.randint(0, 360))
            s = random.randint(0, 5)
            c = random.randint(0, 5)
            bugs[b].shape(shapes[s])
            bugs[b].color(colors[c])

            score += 1              #벌레 먹으면 점수 1 추가
            setScore(score)         #점수판 업데이트
            size += 1
            p.turtlesize(size, size)


screen.mainloop()       #화면 꺼짐 방지