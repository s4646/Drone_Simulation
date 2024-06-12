from PIDController import PIDController

class ChopperController:
    def __init__(self):
        # Initialize PID controllers for pitch, and roll
        self.pitch_pid = PIDController(kp=0.5, ki=0.005, kd=0.05)
        self.roll_pid = PIDController(kp=0.5, ki=0.005, kd=0.05)

    def update(self,
               desired_pitch, current_pitch,
               desired_roll, current_roll):
        
        # Compute control outputs for each axis
        pitch_output = self.pitch_pid.compute(desired_pitch, current_pitch)
        roll_output = self.roll_pid.compute(desired_roll, current_roll)

        # Return the adjusted parameters
        return pitch_output, roll_output