import RPi.GPIO as gpio
import time
import threading

gpio.setmode(gpio.BCM)

# Constants
MOTORPARAMS = {
               'X':{'gear_ratio':1,'step_angle':1.8,'dir_pin':2,'step_pin':3,'enable_pin':14,'wheel_dia':40},
               'Y':{'gear_ratio':1,'step_angle':1.8,'dir_pin':12,'step_pin':17,'enable_pin':14,'wheel_dia':20},
               'L1':{'gear_ratio':5.2,'step_angle':1.8,'dir_pin':18,'step_pin':23,'enable_pin':16,'limit':180},
               'L2':{'gear_ratio':13,'step_angle':1.8,'dir_pin':24,'step_pin':25,'enable_pin':15,'limit':180},
               'L3':{'gear_ratio':5.2,'step_angle':1.8,'dir_pin':20,'step_pin':21,'enable_pin':15,'limit':180},
               'L4':{'gear_ratio':5.2,'step_angle':1.8,'dir_pin':20,'step_pin':21,'enable_pin':15,'limit':180},
               'R1':{'gear_ratio':5.2,'step_angle':1.8,'dir_pin':27,'step_pin':22,'enable_pin':15,'limit':180},
               'R2':{'gear_ratio':19.2,'step_angle':1.8,'dir_pin':10,'step_pin':9,'enable_pin':16,'limit':180},
               'R3':{'gear_ratio':5.2,'step_angle':1.8,'dir_pin':11,'step_pin':5,'enable_pin':16,'limit':180},
               'R4':{'gear_ratio':1,'step_angle':1.8,'dir_pin':6,'step_pin':13,'enable_pin':16,'limit':180},
               'R5':{'gear_ratio':1,'step_angle':1.8,'dir_pin':19,'step_pin':26,'enable_pin':16,'limit':180},
               } # Motor parameters for each motor

lowest_pulsewidth = 0.000625  # lowest pulse width acheivable with the motor

# Initialize arm and linear displacement variables
# These will be used to store the displacement values for each motor
arm_displacement = {'L1':0,'L2':0,'L3':0,'L4':0,'R1':0,'R2':0,'R3':0,'R4':0,'R5':0}
arm_displacement_pulses = {'L1':0,'L2':0,'L3':0,'L4':0,'R1':0,'R2':0,'R3':0,'R4':0,'R5':0}
arm_pulsewidth = {'L1':0,'L2':0,'L3':0,'L4':0,'R1':0,'R2':0,'R3':0,'R4':0,'R5':0}

linear_displacement = {'X':0,'Y':0}
linear_displacement_pulses = {'X':0,'Y':0}
linear_pulsewidth = {'X':0,'Y':0}

# Get user input for arm and linear displacements and calculate the corresponding pulse values
for value in arm_displacement :
    arm_displacement[value] = input(value+':')
    arm_displacement_pulses[value] = (abs(int(arm_displacement[value]))*MOTORPARAMS[value]['gear_ratio'])/MOTORPARAMS[value]['step_angle']
for value in linear_displacement :
    linear_displacement[value] = input(value+':')
    linear_displacement_pulses[value] = (abs(int(linear_displacement[value]))*360*MOTORPARAMS[value]['gear_ratio'])/(MOTORPARAMS[value]['wheel_dia']*3.14*MOTORPARAMS[value]['step_angle'])

# Find the maximum pulse value for arm displacement and linear displacement and set the pulse width accordingly
max_arm_pulse = max(arm_displacement_pulses.values())
max_linear_pulse = max(linear_displacement_pulses.values())

for value in arm_pulsewidth :
        arm_pulsewidth[value] = lowest_pulsewidth * (max_arm_pulse / arm_displacement_pulses[value]) if arm_displacement_pulses[value] != 0 else lowest_pulsewidth

for value in linear_pulsewidth :
        linear_pulsewidth[value] = lowest_pulsewidth * (max_linear_pulse / linear_displacement_pulses[value]) if linear_displacement_pulses[value] != 0 else lowest_pulsewidth


# Enable all motors
for motor in MOTORPARAMS:                               
    gpio.setup(MOTORPARAMS[motor]['enable_pin'], gpio.OUT)
    gpio.output(MOTORPARAMS[motor]['enable_pin'], gpio.LOW)
# Set direction and step pins for each motor
for motor in MOTORPARAMS:                         
    gpio.setup(MOTORPARAMS[motor]['dir_pin'], gpio.OUT)
    gpio.setup(MOTORPARAMS[motor]['step_pin'], gpio.OUT)    

def rotate_motor(motor,pulses,pulsewidth,angle):
    # Set direction based on the angle :
    if int(angle) < 0:
        gpio.output(MOTORPARAMS[motor]['dir_pin'], gpio.LOW)  # Set direction to reverse
    else:
        gpio.output(MOTORPARAMS[motor]['dir_pin'], gpio.HIGH)  # Set direction to forward

    for i in range(int(pulses)):
        gpio.output(MOTORPARAMS[motor]['step_pin'],gpio.HIGH)
        time.sleep(pulsewidth)
        gpio.output(MOTORPARAMS[motor]['step_pin'],gpio.LOW)
        time.sleep(pulsewidth)

# Create threads for each motor with non-zero pulses
threads = []
for motor in arm_displacement_pulses:
    if arm_displacement_pulses[motor] != 0:
        thread = threading.Thread(target=rotate_motor, args=(motor, arm_displacement_pulses[motor], arm_pulsewidth[motor], arm_displacement[motor]))
        threads.append(thread)
        thread.start()
for motor in linear_displacement_pulses:
    if linear_displacement_pulses[motor] != 0:
        thread = threading.Thread(target=rotate_motor, args=(motor, linear_displacement_pulses[motor], linear_pulsewidth[motor], linear_displacement[motor]))
        threads.append(thread)
        thread.start()
# Wait for all threads to finish
for thread in threads:  
    thread.join()   
# Disable all motors after completion
for motor in MOTORPARAMS:
    gpio.output(MOTORPARAMS[motor]['enable_pin'], gpio.HIGH)  # Disable motor