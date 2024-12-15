import RPi.GPIO as GPIO
import time
#class for read ultrasonic sensor hc-sr04
class HCSR04(object):

        def __init__(self, trigger, echo,maxtime = 0.5, board = GPIO.BCM):
                self.trigger = trigger
                self.echo = echo
                self.board = board
                self.maxtime = maxtime
                # Initialize GPIO
                GPIO.setmode(self.board)
                GPIO.setwarnings(False)
                GPIO.setup(self.trigger, GPIO.OUT)
                GPIO.setup(self.echo, GPIO.IN)
        def distance(self):
                # set Trigger to HIGH
                GPIO.output(self.trigger, True)

                # set Trigger after 0.01 ms to LOW
                time.sleep(0.00001)
                GPIO.output(self.trigger, False)

                # Initialize
                StartTime = time.time()
                StopTime = time.time()
                timeout = StartTime + self.maxtime
                # set StartTime
                while GPIO.input(self.echo) == 0 and StartTime <= timeout:
                        StartTime = time.time()

                # set StopTime when arrival
                while GPIO.input(self.echo) == 1 and StopTime <= timeout:
                        StopTime = time.time()

                if StartTime > timeout or StopTime > timeout:
                        # timeout
                        return -1
                else:
                        # time difference between start and stopTimeElapsed
                        TimeDiff = StopTime - StartTime

                        # multiply with the sonic speed (34300 cm/s)
                        # and divide by 2, because there and back
                        return ((TimeDiff * 34300) / 2)

        def clean(self):
                 GPIO.cleanup() # cleanup all GPIO