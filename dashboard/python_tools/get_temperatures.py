from reachy import parts, Reachy
from reachy.utils.discovery import discover_all


def get_temperatures(reachy):

    return message

if __name__ == '__main__':
    if discover_all() == False:
        print()
    reachy = Reachy(head=parts.Head(io='/dev/ttyUSB*'),
                    left_arm=parts.LeftArm(io='/dev/ttyUSB*', hand='force_gripper'),
                    right_arm=parts.RightArm(io='/dev/ttyUSB*', hand='force_gripper'),
    )
    get_temperatures(reachy)
