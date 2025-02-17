"""Robot API."""
import math
import numpy as np
import os

TICKS_PER_RADIANS = 508.8 / (2 * math.pi)  # There are 508.8 ticks per wheel rotation.
TIME_STEP = 32

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Robot:
    """Robot class."""

    _robot = None

    def __init__(self, args: str = "") -> None:
        """Initialize the class.

        Args:
            args: the arguments string.
        """
        self._args = args
        self._realistic = True if os.getenv("ITI0201_REALISTIC", "0") == "1" else False

        self._lidar = Robot._robot.getDevice("rplidar")
        self._lidar.enable(TIME_STEP)
        self._lidar.enablePointCloud()
        
        self.inertial_unit = Robot._robot.getDevice("inertial_unit")
        self.inertial_unit.enable(TIME_STEP)

        self._rgb_camera = Robot._robot.getDevice("rgb_camera")
        self._rgb_camera.enable(TIME_STEP)
        self._rgb_camera_image = None
        self._rgb_camera_image_width = None
        self._rgb_camera_image_retrieved_timestamp = -1

        self._depth_camera = Robot._robot.getDevice("depth_camera")
        self._depth_camera.enable(TIME_STEP)

        self._left_motor = Robot._robot.getDevice("left_wheel_joint")
        self._left_motor.setAcceleration(10)
        self._left_motor.setPosition(float("inf"))

        self._right_motor = Robot._robot.getDevice("right_wheel_joint")
        self._right_motor.setAcceleration(10)
        self._right_motor.setPosition(float("inf"))

        self._left_motor_position = Robot._robot.getDevice("left_wheel_joint_sensor")
        self._left_motor_position.enable(TIME_STEP)

        self._right_motor_position = Robot._robot.getDevice("right_wheel_joint_sensor")
        self._right_motor_position.enable(TIME_STEP)

        self._ir_intensity_center = Robot._robot.getDevice("ir_intensity_center")
        self._ir_intensity_center.enable(TIME_STEP)
        self._ir_intensity_center_right = (
            Robot._robot.getDevice("ir_intensity_center_right")
        )
        self._ir_intensity_center_right.enable(TIME_STEP)
        self._ir_intensity_center_left = (
            Robot._robot.getDevice("ir_intensity_center_left")
        )
        self._ir_intensity_center_left.enable(TIME_STEP)
        self._ir_intensity_side_right = (
            Robot._robot.getDevice("ir_intensity_side_right")
        )
        self._ir_intensity_side_right.enable(TIME_STEP)
        self._ir_intensity_side_left = Robot._robot.getDevice("ir_intensity_side_left")
        self._ir_intensity_side_left.enable(TIME_STEP)
        self._ir_intensity_right = Robot._robot.getDevice("ir_intensity_right")
        self._ir_intensity_right.enable(TIME_STEP)
        self._ir_intensity_left = Robot._robot.getDevice("ir_intensity_left")
        self._ir_intensity_left.enable(TIME_STEP)
        self.WHEEL_BASE = 0.233
        self.TRACK_WIDTH = self.WHEEL_BASE
        self.WHEEL_RADIUS = 0.03575
        self.WHEEL_DIAMETER = self.WHEEL_RADIUS * 2

    def get_time(self) -> float:
        """Return the current elapsed time from the start in seconds.

        Returns:
            The current time in seconds.
        """
        return self._robot.getTime()
        
    def get_orientation(self):
        """Returns the robot's orientation (yaw) from the inertial unit.
        
        Returns:
            The current orientation in radians.
        
        """
        rotation = self.inertial_unit.getRollPitchYaw()
        return rotation[2]

    def get_simulator(self) -> bool:
        """Return whether running in simulator or on real robot.

        Returns:
            True if simulation, False if real robot.
        """
        return True

    def get_realistic(self) -> bool:
        """Return whether running in realistic mode or not.

        Returns:
            True if realistic, False if not.
        """
        return self._realistic

    def get_lidar_range_list(self) -> list:
        """Get the list of lidar range readings.

        Returns:
            A list of distances (in meters) obtained from the lidar sensor.
            The list is ordered clockwise when viewed from above, starting
            from the robot's right side (90 degrees clockwise from the top).
            Each value represents the range at a specific angle.

        """
        if self._realistic:
            range_list = np.array(self._lidar.getRangeImage())
            return ((range_list * np.random.uniform(0.96, 1.04,
                                                    size=range_list.shape)) *
                    np.random.choice([1, np.nan, float('inf')],
                                     size=range_list.shape,
                                     p=[0.996, 0.002, 0.002])).tolist()
        else:
            return self._lidar.getRangeImage()

    def get_lidar_point_cloud(self) -> list:
        """Get the lidar point cloud data.

        Returns:
            A list of objects, where each object represents a point in 3D space.
            Each object contains 'x', 'y', and 'z' attributes corresponding to
            the coordinates of the point in meters, relative to the sensor's position.

        """
        if self._realistic:
            point_cloud = self._lidar.getPointCloud()
            x_values = np.array([point.x for point in point_cloud]) * np.random.uniform(0.96, 1.04, size=len(point_cloud))
            y_values = np.array([point.y for point in point_cloud]) * np.random.uniform(0.96, 1.04, size=len(point_cloud))
            return [Point(x, y, 0.0) for x, y in zip(x_values, y_values)]
        else:
            return self._lidar.getPointCloud()

    def set_left_motor_velocity(self, speed: float) -> None:
        """Set the rotational velocity of the left motor.

        Args:
            speed: The desired rotational velocity for the right motor in radians per
                   second. Positive values indicate forward rotation, while negative
                   values indicate backward rotation.

        """
        if not self._realistic:
            self._left_motor.setVelocity(speed)
        else:
            print("In realistic mode, use set_left_motor_torque() instead!")
            self._left_motor.setVelocity(0)

    def set_right_motor_velocity(self, speed: float) -> None:
        """Set the rotational velocity of the right motor.

        Args:
            speed: The desired rotational velocity for the right motor in radians per
                   second. Positive values indicate forward rotation, while negative
                   values indicate backward rotation.

        """
        if not self._realistic:
            self._right_motor.setVelocity(speed)
        else:
            print("In realistic mode, use set_right_motor_torque() instead!")
            self._right_motor.setVelocity(0)

    def set_left_motor_torque(self, torque: float) -> None:
        """Adjust the torque for the left motor to control its speed and direction.

        This method applies a specified torque to the left motor, influencing both
        its speed and direction. Positive torque results in forward movement, 
        negative torque results in backward movement, and zero torque stops the motor.

        Args:
            torque: The torque value in Newton-meters (Nm), where:
                    - Positive values (> 0 Nm) result in forward movement.
                    - Negative values (< 0 Nm) result in backward movement.
                    - 0 Nm stops the motor.

        """
        self._left_motor.setTorque(torque)

    def set_right_motor_torque(self, torque: float) -> None:
        """Adjust the torque for the right motor to control its speed and direction.

        This method applies a specified torque to the right motor, influencing both
        its speed and direction. Positive torque results in forward movement, 
        negative torque results in backward movement, and zero torque stops the motor.

        Args:
            torque: The torque value in Newton-meters (Nm), where:
                    - Positive values (> 0 Nm) result in forward movement.
                    - Negative values (< 0 Nm) result in backward movement.
                    - 0 Nm stops the motor.

        """
        self._right_motor.setTorque(torque)

    def get_left_motor_encoder_ticks(self) -> int:
        """Return the number of ticks from the right motor encoder.

        Based on documentation at: https://iroboteducation.github.io/create3_docs/api/odometry/

        Returns:
            The number of ticks as an integer.

        """
        return math.floor(TICKS_PER_RADIANS * self._left_motor_position.getValue())

    def get_right_motor_encoder_ticks(self) -> int:
        """Return the number of ticks from the right motor encoder.

        Based on documentation at: https://iroboteducation.github.io/create3_docs/api/odometry/

        Returns:
            The number of ticks as an integer.

        """
        return math.floor(TICKS_PER_RADIANS * self._right_motor_position.getValue())

    def get_camera_field_of_view(self):
        """Returns the camera HFOV (Horizontal Field of View).
        
        Returns:
            FOV in radians.

        """
        return self._rgb_camera.getFov()

    def get_camera_rgb_image(self) -> np.ndarray:
        """Return an image from the camera as a NumPy array in BGRA format.

        This method retrieves the raw image data from the camera's RGB sensor,
        converts it into a NumPy array, and reshapes it into the correct
        dimensions corresponding to the height, width, and number of channels
        (BGRA). The image data is returned in the format (height, width, 4),
        where the last dimension represents the BGRA channels (Blue, Green,
        Red, Alpha).

        Returns:
            A 3D NumPy array of shape (height, width, 4) representing the
            captured BGRA image, with pixel values as unsigned integers.

        """
        return np.frombuffer(
            self._rgb_camera.getImage(),
            dtype=np.uint8,
        ).reshape(self._rgb_camera.getHeight(), self._rgb_camera.getWidth(), 4)

    def get_camera_depth_image(self) -> np.ndarray:
        """Return the depth image data from the camera.

        Returns:
            A 2D NumPy array of shape (height, width) representing the captured
            depth image, with pixel values as float values.

        """
        width = self._depth_camera.getWidth()
        height = self._depth_camera.getHeight()

        return np.ctypeslib.as_array(
            self._depth_camera.getRangeImage(data_type="buffer"),
            (width * height,),
        ).reshape(height, width)

    def get_ir_intensities_list(self) -> list:
        """Return the infra-red sensors intensities as a list.

        Returns:
            The returned list has the following order [left, side_left,
            center_left, center, center_right, side_right, right].

        """
        return [
            self._ir_intensity_left.getValue(),
            self._ir_intensity_side_left.getValue(),
            self._ir_intensity_center_left.getValue(),
            self._ir_intensity_center.getValue(),
            self._ir_intensity_center_right.getValue(),
            self._ir_intensity_side_right.getValue(),
            self._ir_intensity_right.getValue(),
        ]

    def get_ir_intensity_left(self) -> float:
        """Return the leftmost infra-red sensor value.

        Returns:
            The distance value as a float.
            The value range is from 0 (far) to 4000 (close).

        """
        return self._ir_intensity_left.getValue()

    def get_ir_intensity_side_left(self) -> float:
        """Return the second leftmost infra-red sensor value.

        Returns:
            The distance value as a float.
            The value range is from 0 (far) to 4000 (close).

        """
        return self._ir_intensity_side_left.getValue()

    def get_ir_intensity_center_left(self) -> float:
        """Return the third leftmost infra-red sensor value.

        Returns:
            The distance value as a float.
            The value range is from 0 (far) to 4000 (close).

        """
        return self._ir_intensity_center_left.getValue()

    def get_ir_intensity_center(self) -> float:
        """Return the center infra-red sensor value.

        Returns:
            The distance value as a float.
            The value range is from 0 (far) to 4000 (close).

        """
        return self._ir_intensity_center_right.getValue()

    def get_ir_intensity_center_right(self) -> float:
        """Return the third rightmost infra-red sensor value.

        Returns:
            The distance value as a float.
            The value range is from 0 (far) to 4000 (close).

        """
        return self._ir_intensity_center_right.getValue()

    def get_ir_intensity_side_right(self) -> float:
        """Return the second rightmost infra-red sensor value.

        Returns:
            The distance value as a float.
            The value range is from 0 (far) to 4000 (close).

        """
        return self._ir_intensity_side_right.getValue()

    def get_ir_intensity_right(self) -> float:
        """Return the rightmost infra-red sensor value.

        Returns:
            The distance value as a float.
            The value range is from 0 (far) to 4000 (close).

        """
        return self._ir_intensity_right.getValue()

