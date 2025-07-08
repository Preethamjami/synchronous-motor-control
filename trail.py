import RPi.GPIO as gpio
import time
import threading

gpio.setmode(gpio.BCM)

MOTORPARAMS = {
               'X':{'gear_ratio':1,'step_angle':1.8,'dir_pin':2,'step_pin':3,'enable_pin':14,'wheel_dia':40},
               'Y':{'gear_ratio':1,'step_angle':1.8,'dir_pin':12,'step_pin':17,'enable_pin':14,'wheel_dia':20},
               'L1':{'gear_ratio':5.2,'step_angle':1.8,'dir_pin':27,'step_pin':22,'enable_pin':15,'limit':180},
               'L2':{'gear_ratio':13,'step_angle':1.8,'dir_pin':24,'step_pin':25,'enable_pin':15,'limit':180},
               'L3':{'gear_ratio':5.2,'step_angle':1.8,'dir_pin':20,'step_pin':21,'enable_pin':15,'limit':180},
               'L4':{'gear_ratio':5.2,'step_angle':1.8,'dir_pin':20,'step_pin':21,'enable_pin':15,'limit':180},
               'R1':{'gear_ratio':5.2,'step_angle':1.8,'dir_pin':18,'step_pin':23,'enable_pin':16,'limit':180},
               'R2':{'gear_ratio':19.2,'step_angle':1.8,'dir_pin':10,'step_pin':9,'enable_pin':16,'limit':180},
               'R3':{'gear_ratio':5.2,'step_angle':1.8,'dir_pin':11,'step_pin':5,'enable_pin':16,'limit':180},
               'R4':{'gear_ratio':1,'step_angle':1.8,'dir_pin':6,'step_pin':13,'enable_pin':16,'limit':180},
               'R5':{'gear_ratio':1,'step_angle':1.8,'dir_pin':19,'step_pin':26,'enable_pin':16,'limit':180},
               }

arm_displacement = {'L1':0,'L2':0,'L3':0,'L4':0,'R1':0,'R2':0,'R3':0,'R4':0,'R5':0}
linear_displacement = {'X':0,'Y':0}

for value in arm_displacement :
    arm_displacement[value] = input(value+':')
for value in linear_displacement :
    linear_displacement[value] = input(value+':')


motor1 = input('choose motor1')
motor2 = input('choose motor2')
angle = input('angle')
def rotate_motor(motor,required_angle,highest_gearratio = 19.2) :
    #MOTOR_PINS = [15, 27, 22]
    MOTOR_PINS = [MOTORPARAMS[motor]['enable_pin'], MOTORPARAMS[motor]['dir_pin'],MOTORPARAMS[motor]['step_pin']]

    for pin in MOTOR_PINS:
        gpio.setup(pin, gpio.OUT)

    #parameters
    # step_angle = 1.8
    # gear_ratio = 19.2
    effective_angle = MOTORPARAMS[motor]['step_angle']/MOTORPARAMS[motor]['gear_ratio']
    pulsesforfullrev = 360/effective_angle
    pulses = pulsesforfullrev*(int(required_angle)/360)


    gpio.output(MOTORPARAMS[motor]['enable_pin'],gpio.LOW)
    gpio.output(MOTORPARAMS[motor]['dir_pin'],gpio.HIGH)

    for i in range(int(pulses)):
        gpio.output(MOTORPARAMS[motor]['step_pin'],gpio.HIGH)
        time.sleep(0.000625*(highest_gearratio/MOTORPARAMS[motor]['gear_ratio']))
        gpio.output(MOTORPARAMS[motor]['step_pin'],gpio.LOW)
        time.sleep(0.000625*(highest_gearratio/MOTORPARAMS[motor]['gear_ratio']))

    gpio.output(MOTORPARAMS[motor]['dir_pin'],gpio.LOW)

    for i in range(int(pulses)):
        gpio.output(MOTORPARAMS[motor]['step_pin'],gpio.HIGH)
        time.sleep(0.000625*(19.2/MOTORPARAMS[motor]['gear_ratio']))
        gpio.output(MOTORPARAMS[motor]['step_pin'],gpio.LOW)
        time.sleep(0.000625*(19.2/MOTORPARAMS[motor]['gear_ratio']))

thread1 = threading.Thread(target=rotate_motor, args=(motor1, angle))
#thread2 = threading.Thread(target=rotate_motor, args=(motor2, angle))

# Start threads
thread1.start()
#thread2.start()

# Wait for threads to finish
thread1.join()
#thread2.join()