import requests

token = "your token here"
url = "http://127.0.0.1:8801/api/v1/robot-motors/"


# l, r - параметры ШИМа для левого и правого мотора соответсвенно; l_time, r_time - время работы моторов
def move(l=0, l_time=0, r=0, r_time=0):
    requests.post(
        f"{url}move?l={l}&l_time={l_time}&r={r}&r_time={r_time}&token={token}")


def get_sensor_data():
    data = requests.get(f"{url}sensor-data?token={token}").json()
    front_dist = data["front_distance"]
    back_dist = data["back_distance"]
    left_45_dist = data["left_45_distance"]
    right_45_dist = data["right_45_distance"]
    left_side_dist = data["left_side_distance"]
    right_side_dist = data["right_side_distance"]
    yaw = data["rotation_yaw"]  # поворот
    return [front_dist, back_dist, left_45_dist, right_45_dist, left_side_dist, right_side_dist, yaw]


def restart():
    requests.post(f"http://127.0.0.1:8801/api/v1/maze/restart?token={token}")