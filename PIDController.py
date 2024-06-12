class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.prev_error = 0
        self.integral = 0

    def compute(self, setpoint, current_value):
        error = setpoint - current_value

        # Proportional term
        p_term = self.kp * error

        # Integral term
        self.integral += error
        i_term = self.ki * self.integral

        # Derivative term
        d_term = self.kd * (error - self.prev_error)
        self.prev_error = error

        # Control output
        control_output = p_term + i_term + d_term
        return control_output