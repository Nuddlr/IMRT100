# Example code for IMRT100 robot project


# Import some modules that we need
import pygame
import RPi.GPIO
import imrt_robot_serial
import signal
import time
import sys


# We want our program to send commands at 10 Hz (10 commands per second)
execution_frequency = 10 #Hz
execution_period = 1. / execution_frequency #seconds


# Create motor serial object
motor_serial = imrt_robot_serial.IMRTRobotSerial()


# Open serial port. Exit if serial port cannot be opened
try:
    motor_serial.connect("/dev/ttyACM0")
except:
    print("Could not open port. Is your robot connected?\nExiting program")
    sys.exit()

    
# Start serial receive thread
motor_serial.run()

#################
# Eksempel GRUPPE1
# Servo setup

servoPIN_1 = 17
servoPIN_2 = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN_1, servoPIN_2, GPIO.OUT)

hand_left = GPIO.PWM(servoPIN_1, 50) # GPIO 17 for PWM with 50Hz
hand_left.start(2.5) # Initialization
hand_right = GPIO.PWM(servoPIN_2, 50) # GPIO 18 for PWM with 50Hz
########################

# Now we will enter a loop that will keep looping until the program terminates
# The motor_serial object will inform us when it's time to exit the program
# (say if the program is terminated by the user)
print("Entering loop. Ctrl+c to terminate")
while not motor_serial.shutdown_now :


    ###############################################################
    # This is the start of our loop. Your code goes below.        #
    #                                                             #
    # An example is provided to give you a starting point         #
    # In this example we get the distance readings from each of   #
    # the two distance sensors. Then we multiply each reading     #
    # with a constant gain and use the two resulting numbers      #
    # as commands for each of the two motors.                     #
    #  ________________________________________________________   #
    # |                                                        |  #
    # V                                                           #
    # V                                                           #
    ###############################################################


    # Get the current time
    iteration_start_time = time.time()



    # Get and print readings from distance sensors
    dist_1 = motor_serial.get_dist_1()
    dist_2 = motor_serial.get_dist_2()
    print("Dist 1:", dist_1, "   Dist 2:", dist_2)

    

    # Calculate commands for each motor using sensor readings
    # In this simple example we will multiply each sensor reading
    # with a constant to obtain our commands
    gain = 8
    speed_motor_1 = dist_1 * gain
    speed_motor_2 = dist_2 * gain


    ########
    # Eksempel GRUPPE 1
    # Play sound and move hands if motor speed exceeds eg. 300
    ########
    
    if (speed_motor_1 + speed_motor_2)/2 >= 300:
        #Play sound
        pygame.mixer.init()
        pygame.mixer.music.load("myFile.wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue

        #Move hands
        servoPIN_1.ChangeDutyCycle()
        servoPIN_2.ChangeDutyCycle()
    else:
        #Move hands to initial position
        servoPIN_1.ChangeDutyCycle()
        ServoPIN_2.ChangeDutyCycle()



    # Send commands to motor
    # Max speed is 400.
    # E.g.a command of 500 will result in the same speed as if the command was 400
    motor_serial.send_command(speed_motor_1, speed_motor_2)



    # Here we pause the execution of the program for the apropriate amout of time
    # so that our loop executes at the frequency specified by the variable execution_frequency
    iteration_end_time = time.time() # current time
    iteration_duration = iteration_end_time - iteration_start_time # time spent executing code
    if (iteration_duration < execution_period):
        time.sleep(execution_period - iteration_duration)



    ###############################################################
    #                                                           A #
    #                                                           A #
    # |_________________________________________________________| #
    #                                                             #
    # This is the end of our loop,                                #
    # execution continus at the start of our loop                 #
    ###############################################################
    ###############################################################





# motor_serial has told us that its time to exit
# we have now exited the loop
# It's only polite to say goodbye
p.stop()
GPIO.cleanup()
print("Goodbye")
