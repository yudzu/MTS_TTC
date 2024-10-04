import requests

token = "your token here"
url = "http://127.0.0.1:8801/api/v1/robot-cells/"


def move_forward():
    requests.post(f"{url}forward?token={token}")


def move_backward():
    requests.post(f"{url}backward?token={token}")


def turn_left():
    requests.post(f"{url}left?token={token}")


def turn_right():
    requests.post(f"{url}right?token={token}")


def get_sensor_data():
    data = requests.get(f"{url}sensor-data?token={token}").json()
    front_dist = data["front_distance"]
    back_dist = data["back_distance"]
    left_side_dist = data["left_side_distance"]
    right_side_dist = data["right_side_distance"]
    yaw = data["rotation_yaw"]  # поворот
    return [front_dist, back_dist, left_side_dist, right_side_dist, yaw]


def send_result(matrix):
    return requests.post(f"http://127.0.0.1:8801/api/v1/matrix/send?token={token}", json=matrix).json()


def compare_data_to_wall(f, b, l, r):
    if f > 80 and b > 80 and l > 80 and r > 80:
        return 0
    elif f > 80 and b > 80 and l < 80 and r > 80:
        return 1
    elif f < 80 and b > 80 and l > 80 and r > 80:
        return 2
    elif f > 80 and b > 80 and l > 80 and r < 80:
        return 3
    elif f > 80 and b < 80 and l > 80 and r > 80:
        return 4
    elif f > 80 and b < 80 and l < 80 and r > 80:
        return 5
    elif f > 80 and b < 80 and l > 80 and r > 80:
        return 6
    elif f < 80 and b > 80 and l > 80 and r < 80:
        return 7
    elif f < 80 and b > 80 and l < 80 and r > 80:
        return 8
    elif f > 80 and b > 80 and l < 80 and r < 80:
        return 9
    elif f < 80 and b < 80 and l > 80 and r > 80:
        return 10
    elif f < 80 and b < 80 and l > 80 and r < 80:
        return 11
    elif f < 80 and b > 80 and l < 80 and r < 80:
        return 12
    elif f < 80 and b < 80 and l < 80 and r > 80:
        return 13
    elif f > 80 and b < 80 and l < 80 and r < 80:
        return 14
    elif f < 80 and b < 80 and l < 80 and r < 80:
        return 15


def get_wall(f, b, l, r, y):
    if -45 < y < 45:  # вверх
        return compare_data_to_wall(f, b, l, r)
    elif 45 < y < 135:  # вправо
        return compare_data_to_wall(l, r, b, f)
    elif -225 < y < -135:  # вниз
        return compare_data_to_wall(b, f, r, l)
    elif -135 < y < -45:  # влево
        return compare_data_to_wall(r, l, f, b)


# расстояние между центрами двух клеток ~167
i, j = 15, 0
maze = [[0 for _ in range(16)] for _ in range(16)]
flag = True
# РЕШЕНИЕ МЕТОДОМ ПРАВОЙ РУКИ
while flag:
    print(get_sensor_data())
    front_dist, back_dist, left_side_dist, right_side_dist, yaw = get_sensor_data()
    maze[i][j] = get_wall(front_dist, back_dist, left_side_dist, right_side_dist, yaw)
    if right_side_dist > 80:
        turn_right()
        move_forward()
    elif front_dist > 80:
        move_forward()
    else:
        turn_right()
        turn_right()
    enough = True
    for row in maze:
        if 0 in row:
            enough = False
            break
    flag = ~enough
print(maze)
print(send_result(maze))
