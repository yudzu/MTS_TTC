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
