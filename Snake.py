import turtle
import random
from functools import partial

g_screen = None
g_snake = None
g_snake_body = [(0, 0)]
g_monster = None
g_snake_sz = 4
g_intro = None
g_keypressed = None
g_status = None
time = 0
c_num = 0
g_contact = None
g_time = None
g_food_items = []
space_status = 0
toward_status = 0
food_item_font = ("Arial", 10, "normal")

COLOR_BODY = ("blue", "black")
COLOR_HEAD = "red"
COLOR_MONSTER = "purple"
FONT = ("Arial", 16, "normal")

KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_SPACE = \
    "Up", "Down", "Left", "Right", "space"

HEADING_BY_KEY = {KEY_UP: 90, KEY_DOWN: 270, KEY_LEFT: 180, KEY_RIGHT: 0}


def configurePlayArea():
    # 创建游戏区域的函数，包括动作和状态边界、游戏介绍信息和状态显示。
    # 运动边界
    m = createTurtle(0, 0, "", "black")
    m.shapesize(25, 25, 5)
    m.goto(0, -40)  # shift down half the status

    # 状态边界
    s = createTurtle(0, 0, "", "black")
    s.shapesize(4, 25, 5)
    s.goto(0, 250)  # shift up half the motion

    # introduction
    intro = createTurtle(-200, 150)
    intro.hideturtle()
    intro.write("Click anywhere to start the game .....", font=("Arial", 16, "normal"))

    # statuses
    status_m = createTurtle(0, 0, "", "black")
    status_m.hideturtle()
    status_m.goto(50, s.ycor() - 20)

    time_m = createTurtle(0, 0, "red", "black")
    time_m.hideturtle()
    time_m.goto(-80, s.ycor() - 20)

    contact_m = createTurtle(0, 0, "red", "black")
    contact_m.hideturtle()
    contact_m.goto(-240, s.ycor() - 20)

    return intro, status_m, time_m, contact_m


def configScreen():
    # 配置turtle屏幕的函数，包括设置标题、大小和模式。
    s = turtle.Screen()
    s.tracer(0)  # disable auto screen refresh, 0=disable, 1=enable
    s.title("Snake by Kinley Lam")
    s.setup(500 + 80, 500 + 120 + 80)
    s.mode("standard")
    return s


def createTurtle(x, y, color="red", border="black"):
    # 一个用给定坐标和颜色创建turtle对象的函数。
    t = turtle.Turtle("square")
    t.color(border, color)
    t.up()
    t.goto(x, y)
    return t


def updateStatus():
    # 使用用户按下的最后一个箭头键更新状态显示的函数。
    g_status.clear()
    g_status.write('Motion : {}'.format(g_keypressed), font=('arial', 18, 'bold'))
    g_screen.update()


def updateTimes():
    g_time.clear()
    g_time.write('Time : {}'.format(time), font=('arial', 18, 'bold'))
    g_screen.update()


def updateContact():
    g_contact.clear()
    g_contact.write('Contact : {}'.format(c_num), font=('arial', 18, 'bold'))
    g_screen.update()


def setSnakeHeading(key):
    # 一个基于用户按下的箭头键来设置蛇的方向的函数。
    if key in HEADING_BY_KEY.keys():
        g_snake.setheading(HEADING_BY_KEY[key])


def onArrowKeyPressed(key):
    # 当按下箭头键时调用的函数。它设置g_keypressed变量并相应地更新蛇头和状态显示。
    global g_keypressed, space_status, toward_status
    g_keypressed = key
    if key == 'space':
        space_status = (space_status + 1) % 2
    if key != 'space' and space_status == 1 and toward_status == 0:
        toward_status = 0
        space_status = 0
    setSnakeHeading(key)
    updateStatus()


def towards():
    if len(g_snake_body) > 0:
        if g_snake_body[4][1] == g_snake_body[3][1]:
            if g_snake_body[4][0] > g_snake_body[3][0]:
                return 'Right'
            elif g_snake_body[4][0] < g_snake_body[3][0]:
                return 'Left'
        elif g_snake_body[4][0] == g_snake_body[3][0]:
            if g_snake_body[4][1] > g_snake_body[3][1]:
                return 'Up'
            elif g_snake_body[4][1] < g_snake_body[3][1]:
                return 'Down'
    return None


def onTimerSnake():
    # 由turtle屏幕的计时器调用的函数，用于更新蛇的位置和外观。
    global g_snake_sz, space_status
    snakev = 200
    if game_over():
        return
    if not inside_body():
        g_screen.ontimer(onTimerSnake, 200)
        return
    if not inside():
        if towards() == 'Right':
            if -260 < g_snake.ycor() < 180 and g_keypressed in ('Up','Down') or \
                    g_snake.ycor() >= 180 and (g_snake.xcor() <= 220 and g_keypressed in ('Right','Down','space') or g_snake.xcor() > 220 and g_keypressed in ('Down')) or \
                    g_snake.ycor() <= -260 and (g_snake.xcor() <= 220 and g_keypressed in ('Right','Up','space') or g_snake.xcor() > 220 and g_keypressed in ('Up')):
                print(1)
                pass
            else:
                g_screen.ontimer(onTimerSnake, 200)
                return
        elif towards() == 'Left':
            if -260 < g_snake.ycor() < 180 and g_keypressed in ('Up','Down') or \
                    g_snake.ycor() >= 180 and (g_snake.xcor() >= -220 and g_keypressed in ('Left','Down','space') or g_snake.xcor() < -220 and g_keypressed in ('Down')) or \
                    g_snake.ycor() <= -260 and (g_snake.xcor() >= -220 and g_keypressed in ('Left','Up','space') or g_snake.xcor() < -220 and g_keypressed in ('Up')):
                print(2)
                pass
            else:
                g_screen.ontimer(onTimerSnake, 200)
                return
        elif towards() == 'Up':
            if -220 < g_snake.xcor() < 220 and g_keypressed in ('Left','Right') or \
                    g_snake.xcor() >= 220 and (g_snake.ycor() <= 180 and g_keypressed in ('Left','Up','space') or g_snake.ycor() > 180 and g_keypressed in ('Left')) or \
                    g_snake.xcor() <= -220 and (g_snake.ycor() <= 180 and g_keypressed in ('Right','Up','space') or g_snake.ycor() > 180 and g_keypressed in ('Right')):
                print(3)
                pass
            else:
                g_screen.ontimer(onTimerSnake, 200)
                return
        elif towards() == 'Down':
            if -220 < g_snake.xcor() < 220 and g_keypressed in ('Left','Right') or \
                    g_snake.xcor() >= 220 and (g_snake.ycor() >= -260 and g_keypressed in ('Left','Down','space') or g_snake.ycor() < -260 and g_keypressed in ('Left')) or \
                    g_snake.xcor() <= -220 and (g_snake.ycor() >= -260 and g_keypressed in ('Right','Down','space') or g_snake.ycor() < -260 and g_keypressed in ('Right')):
                print(4)
                pass
            else:
                g_screen.ontimer(onTimerSnake, 200)
                return
        else:
            g_screen.ontimer(onTimerSnake, 200)
            return
    g_snake.goto(round(g_snake.xcor()), round(g_snake.ycor()))

    if space_status == 1 and space_status == 0:
        g_screen.ontimer(onTimerSnake, 200)
        return

    if (space_status + toward_status) % 2 == 0:
        # Clone the head as body
        g_snake.color(*COLOR_BODY)
        g_snake.stamp()
        g_snake.color(COLOR_HEAD)

        # Advance snake
        g_snake.forward(20)
        g_snake_body.append((round(g_snake.xcor()), round(g_snake.ycor())))
        csf, fn = check_snake_food()
        if csf:
            g_snake_sz += fn
        # Shifting or extending the tail.
        # Remove the last square on Shifting.
        if len(g_snake.stampItems) > g_snake_sz:
            g_snake.clearstamps(1)
            g_snake_body.pop(0)
        # print('g_snake_body:{}, 长度：{}'.format(g_snake_body,len(g_snake_body)))
        snakev = round(200 * (g_snake_sz / 7))
    g_screen.update()
    g_screen.ontimer(onTimerSnake, snakev)


def onTimerMonster():
    # 由turtle屏幕的计时器调用的函数，用于更新怪物的位置和外观。
    # print('onTimerMonster')
    if game_over():
        return
    min = g_monster.distance(g_snake.xcor() - 20, g_snake.ycor())
    minindex = 0
    if not min < g_monster.distance(g_snake.xcor(), g_snake.ycor() - 20):
        minindex = 90
        min = g_monster.distance(g_snake.xcor(), g_snake.ycor())
    if not min < g_monster.distance(g_snake.xcor() + 20, g_snake.ycor()):
        minindex = 180
        min = g_monster.distance(g_snake.xcor() + 20, g_snake.ycor())
    if not min < g_monster.distance(g_snake.xcor(), g_snake.ycor() + 20):
        minindex = 270
        min = g_monster.distance(g_snake.xcor(), g_snake.ycor() + 20)
    g_monster.setheading(minindex)
    g_monster.forward(20)
    onTimerContact()
    # print(c_num)
    monsterv = random.randint(300, 400)
    g_screen.update()
    g_screen.ontimer(onTimerMonster, monsterv)


def onTimer():
    global time
    # print('onTimer')
    if game_over():
        return
    time += 1
    updateTimes()
    g_screen.update()
    g_screen.ontimer(onTimer, 1000)


def onTimerContact():
    global c_num
    # print('onTimerContact')
    if game_over():
        return
    if m_s():
        c_num += 1
    updateContact()
    g_screen.update()


def onTimerHide():
    # print('还有多少食物：', len(g_food_items))
    if game_over():
        return
    if len(g_food_items) >= 1:
        n = random.randint(0, len(g_food_items) - 1)
        if g_food_items[n]['status'] == 'visible':
            g_food_items[n]['status'] = 'unvisible'
            g_food_items[n]['foodturtle'].undo()
        elif g_food_items[n]['status'] == 'unvisible':
            g_food_items[n]['status'] = 'visible'
            g_food_items[n]['foodturtle'].write(g_food_items[n]['num'], align='center', font=food_item_font)
        g_screen.ontimer(onTimerHide, 5000)
    return


def startGame(x, y):
    # 这个函数通过隐藏游戏介绍信息、注册箭头键处理程序和启动蛇和怪物计时器来开始游戏。
    g_screen.onscreenclick(None)
    g_intro.clear()

    g_screen.onkey(partial(onArrowKeyPressed, KEY_UP), KEY_UP)
    g_screen.onkey(partial(onArrowKeyPressed, KEY_DOWN), KEY_DOWN)
    g_screen.onkey(partial(onArrowKeyPressed, KEY_LEFT), KEY_LEFT)
    g_screen.onkey(partial(onArrowKeyPressed, KEY_RIGHT), KEY_RIGHT)
    g_screen.onkey(partial(onArrowKeyPressed, KEY_SPACE), KEY_SPACE)

    g_screen.ontimer(onTimerSnake, 100)
    g_screen.ontimer(onTimerMonster, 1000)
    g_screen.ontimer(onTimer, 1000)
    g_screen.ontimer(onTimerHide, 5000)

    createFood()


def createFood():
    # 生成5个食物
    i = 1
    food = [(0, 0)]
    while len(g_food_items) <= 4:
        x = random.randint(-10, 10) * 20
        y = random.randint(-8, 8) * 20 - 7
        if (x, y) in food:
            continue
        food.append((x, y))
        g_food = createTurtle(x, y, 'green')
        food_items = {"num": i, "x": x, "y": y, "status": "visible", 'foodturtle': g_food}
        g_food_items.append(food_items)
        g_food.hideturtle()
        g_food.write(i, align='center', font=food_item_font)
        i += 1
    return g_food_items


def inside():
    # 撞墙检测
    if -220 <= g_snake.xcor() <= 220 and -260 <= g_snake.ycor() <= 180:
        return True
    else:
        return False
    # if g_snake.xcor() > 220 and (g_keypressed == 'Right' or g_keypressed == 'space'):
    #     return False
    # elif g_snake.xcor() < -220 and (g_keypressed == 'Left' or g_keypressed == 'space'):
    #     return False
    # elif g_snake.ycor() > 180 and (g_keypressed == 'Up' or g_keypressed == 'space'):
    #     return False
    # elif g_snake.ycor() < -260 and (g_keypressed == 'Down' or g_keypressed == 'space'):
    #     return False
    # elif g_keypressed is None:
    #     return False
    # else:
    #     return True


def inside_body():
    h = g_snake.heading()
    # print('g_snake.heading : {}  g_snake.xcor : {}  g_snake.ycor : {}'.format(g_snake.heading(),g_snake.xcor(),g_snake.ycor()))
    if h == 0 and ((round(g_snake.xcor()) + 20, round(g_snake.ycor())) not in g_snake_body):
        return True
    elif h == 90 and ((round(g_snake.xcor()), round(g_snake.ycor()) + 20) not in g_snake_body):
        return True
    elif h == 180 and ((round(g_snake.xcor()) - 20, round(g_snake.ycor())) not in g_snake_body):
        return True
    elif h == 270 and ((round(g_snake.xcor()), round(g_snake.ycor()) - 20) not in g_snake_body):
        return True
    return False


def m_s():
    for snake in g_snake_body:
        # print('snake[0]: {}   snake[1]: {}'.format(snake[0],snake[1]))
        if g_monster.distance(snake[0], snake[1]) < 20:
            return True

    return False


def check_snake_food():
    for food in g_food_items:
        if int(g_snake.xcor()) == food['x'] and int(g_snake.ycor()) == food['y'] + 7 and food['status'] == 'visible':
            food['foodturtle'].clear()
            g_food_items.remove(food)
            return True, food['num']
    return False, 0


def game_over():
    if len(g_food_items) == 0:
        g_snake.write('     Snake Win!!!!!', font=('arial', 18, 'bold'))
        return True
    elif g_monster.distance(g_snake.xcor(), g_snake.ycor()) < 20:
        g_monster.write('     Monster Win!!!!', font=('arial', 18, 'bold'))
        return True
    return False


if __name__ == "__main__":
    g_screen = configScreen()
    g_intro, g_status, g_time, g_contact = configurePlayArea()

    updateStatus()
    updateTimes()
    updateContact()

    g_monster = createTurtle(-110, -110, "purple", "black")
    g_snake = createTurtle(0, 0, "red", "black")

    g_screen.onscreenclick(startGame)
    g_screen.update()
    g_screen.listen()

    g_screen.mainloop()
