from PIDController import PIDController

class ChopperController:
    def __init__(self):
        # Initialize PID controllers for yaw, pitch, and roll
        # self.yaw_pid = PIDController(kp=0.1, ki=0.001, kd=0.01)
        self.pitch_pid = PIDController(kp=0.1, ki=0.001, kd=0.01)
        self.roll_pid = PIDController(kp=0.1, ki=0.001, kd=0.01)

    def update(self, #desired_yaw_rate, current_yaw_rate,
               desired_pitch_angle, current_pitch_angle,
               desired_roll_angle, current_roll_angle):
        
        # Compute control outputs for each axis
        #yaw_output = self.yaw_pid.compute(desired_yaw_rate, current_yaw_rate)
        pitch_output = self.pitch_pid.compute(desired_pitch_angle, current_pitch_angle)
        roll_output = self.roll_pid.compute(desired_roll_angle, current_roll_angle)

        # Return the adjusted parameters
        return pitch_output, roll_output # yaw_output