from reachy import parts
from reachy.io.luos import SharedLuosIO


def reachy_temperature(dummy=True):
    if dummy:
        return {'left_arm': {'status': 'ok', 
                            'temp': {'shoulder_pitch': 38.0, 'shoulder_roll': 40.0, 
                            'arm_yaw': 40.0, 'elbow_pitch': 39.0, 'forearm_yaw': 33.0, 
                            'wrist_pitch': 37.0, 'wrist_roll': 36.0, 'gripper': 36.0}}, 
                'head': {'status': 'ok', 
                        'temp': {'disk_top': 0.0, 'disk_middle': 27.062, 'disk_bottom': 0.0}}, 
                'right_arm': {'status': 'ok', 
                        'temp': {'shoulder_pitch': 40.0, 'shoulder_roll': 35.0, 
                        'arm_yaw': 40.0, 'elbow_pitch': 35.0, 'forearm_yaw': 33.0,
                        'wrist_pitch': 37.0, 'wrist_roll': 36.0, 'gripper': 37.0}}}

    SharedLuosIO.close_all_cached_gates()

    try:
        left_arm, left_arm_status = parts.LeftArm(io='/dev/ttyUSB*', hand='force_gripper'), 'ok'
    except (LuosGateNotFoundError, LuosModuleNotFoundError, CameraNotFoundError):
        left_arm, left_arm_status = None, 'missing'

    try:
        head, head_status = parts.Head(io='/dev/ttyUSB*'), 'ok'
    except (LuosGateNotFoundError, LuosModuleNotFoundError, CameraNotFoundError):
        head, head_status = None, 'missing'

    try:
        right_arm, right_arm_status = parts.RightArm(io='/dev/ttyUSB*', hand='force_gripper'), 'ok'
    except (LuosGateNotFoundError, LuosModuleNotFoundError, CameraNotFoundError):
        right_arm, right_arm_status = None, 'missing'

    left_temp, right_temp, head_temp = {}, {}, {}

    if left_arm_status == 'ok':
        left_temp = {m.name.split('.')[-1]: m.temperature for m in left_arm.motors}
        left_arm.teardown()
    if right_arm_status == 'ok':
        right_temp = {m.name.split('.')[-1]: m.temperature for m in right_arm.motors}
        right_arm.teardown()
    if head_status == 'ok':
        head_temp = {d.name: d.temperature for d in head.neck.disks}
        head.teardown()

    left_msg = {'status': left_arm_status, 'temp': left_temp}
    right_msg = {'status': right_arm_status, 'temp': right_temp}
    head_msg = {'status': head_status, 'temp': head_temp}

    temp_msg = {'left_arm': left_msg, 'head': head_msg, 'right_arm': right_msg}

    return(temp_msg)


if __name__ == '__main__':
    print(get_temperature())