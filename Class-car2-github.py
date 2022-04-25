#----------------
# Developed by: Tony Rahman
# Simulation a car travelling and somewhat controlled by the user.
# Implemented using class object, properties, and methods.
# For Class sample examples; see Class-car.py and classes.py
# 
# And uses matplotlib to generate five plots for real-time analytics.
# 
# Updates arrays for plots' x,y coordinates at every loop for each plot.
# Then at user-command for seeing plot (anytime), 5 plots are shown in one window in a grid (using subplot())
# The plot can be externally saved as an image if desired from the window.
# 
# Text in shell is color-coded using ANSI sequence (or by using colorama library...currently commented out but tested and works...the print() calls are different with colorama and
# are currently commented out because I'm using ANSI escape sequences with print.
# 
#
# Blog: http://flyingsalmon.net/?p=3444


#_________CLASS DEFINITION_______________________________________________________________________

class Car:
    def __init__(self, speed=0): 
        self.speed = speed 
        self.odometer = 0 
        self.drivetime = 0 
        self.maxtank = 20.0 
        self.mpg = 40.0 # Miles/gallon
        self.topspeed = 100 # max speed MPH. NOTE THIS IS IN HOUR time unit
        self.engine=0 # engine is OFF by default
        self.avtank=self.maxtank 
        self.usedgas=0  
        self.range=round(self.maxtank * self.mpg, 3)
        self.acceleration = 20 
        self.deceleration = 25 
        self.optimalmpg=(30,60) 
#_____________________________________________________________________________________________
    def get_curr_speed(self): 
        return self.speed    
#_____________________________________________________________________________________________
    def accelerate(self): # A
        global GAMERUNNING
        
        status=""
        if GAMERUNNING==0:
            status="Thanks for playing!"
            GameOver(status, "accelerate()")
        
        if (self.engine): # if engine is ON    
            if (self.speed <= self.topspeed - self.acceleration):
                self.speed += self.acceleration 
                status="OK."                        
            else:
                status="@ Max. speed:" + str(self.topspeed)
            
        else: # engine not ON
            status="Engine is OFF! Start engine, then accelerate to move."
        
        
        return status
#_____________________________________________________________________________________________
    def brake(self): # S
        
        global GAMERUNNING
        
        status=""
        if GAMERUNNING==0:
            status="Thanks for playing!"
            GameOver(status, "brake()")

        if (self.engine):
            if self.speed < self.deceleration:
                self.speed = 0
                status="@Minimum speed:"
            else:
                self.speed -= self.deceleration
                status="Speed reduced."
                
        if self.speed <0: self.speed=0                         

        return status 
    
        
#_____________________________________________________________________________________________
    def step(self):
        # called from main driver's while loop.
        # actionkey: user-pressed key (command). We use this to prevent incrementing time when user is doing any of the following:
        #        checking stats: command/action = T
        #        checking car spec: command/action = I
        #        plotting: command/action = P
        # NOTE that actionkey value is passed as UPPER-case from main driver.
        
        # Update the odometer and time.
        # incremented after each input, goes to next time unit (e.g. next loop. self.drivetime +1)       
        
        # Time (selfetime) is incremented by 1 time unit every time this is called from the main driver...
        # HOWEVER, we don't want time to increment if use is checking stat (T) or specs (I)!
        # So, we check the actionkey before deciding to increment self.drivetime

        global GAMERUNNING
        global MIN_GAS_BEFORE_DIE

        if GAMERUNNING==0:
            GameOver("<unknown end>", "step()-GAMERUNNING==0") # this condition should not happen.
        
        self.odometer += self.speed 
        self.odometer = round(self.odometer, 3)
               
        if (self.speed> 0):
            self.drivetime += 1 
        
        # Calculate used gas (normal x1 rate)
        if (self.speed >0 or self.engine >0): # if engine is running but speed is 0, it still uses gas!
            self.usedgas = self.odometer/self.mpg 
            self.usedgas = round(self.usedgas, 3)
            if self.speed <self.optimalmpg[0] or self.speed > self.optimalmpg[1]:
                self.usedgas = self.usedgas + (self.usedgas * 0.10)  # additional 10% gas usage when outside of optimal speed
                self.usedgas = round(self.usedgas, 2) 

        self.avtank = self.maxtank - self.usedgas
        self.avtank=round(self.avtank, 3)
        if (self.avtank <0):
            self.avtank=0 

        if (self.usedgas >0): # avoid div by zero
            self.mpg=self.odometer/self.usedgas
            self.mpg=round(self.mpg, 3)
            if (DEBUG):
                print("step():MPG:", self.mpg)
        
        if (DEBUG):
            print("step():USED GAS:", self.usedgas) 
            print("step():ODOMETER:", self.odometer)
            print("step():AVTANK:", self.avtank) 
                           
       
       # Populate plot arrays..............................................................       
        global x1, y1, x2, y2, x3, y3, x4, y4
                
        x1.append(self.speed)
        y1.append(self.drivetime)
        x2=x1 # make it point to the same list as x1 since it's also speed but for plot 2.
        y2.append(self.avtank)
        x3.append(self.odometer)
        y3=y2 # make it point to the same list as y3 since it's also avtank but for plot 3.
        x4=x1 # make it point to the same list as x1 since it's also speed but for plot 4.
        y4=x3 # make it point to the same list as x3 since it's also odometer but for plot 4.
        x5.append(self.average_speed()) # NOTE this is a method that returns running average speed, DIFFERENT from self.speed which is current speed in an interation.
        y5.append(self.mpg) 
            

        if self.avtank<MIN_GAS_BEFORE_DIE:
            GAMERUNNING=0
            self.avtank=0 # prevent negative in all cases.
            self.speed = 0
            self.engine=0
            GameOver("Out of gas!", "step()-self.avtank<MIN_GAS_BEFORE_DIE")            


        return
#_____________________________________________________________________________________________
    def average_speed(self): # V. caculated.
        if self.drivetime!=0: 
            avgspd=self.odometer / self.drivetime # mph and time, loop are all in same time unit: 1 hour=1 loop
            return round(avgspd, 3)
        else:
            return 0 # avoid div by zero.
    
#_____________________________________________________________________________________________        
    def start(self):
        # Called when Engine start is pressed (E) by user
        global GAMERUNNING
        global MIN_GAS_BEFORE_DIE
        
        code="" 
        if not GAMERUNNING:
            code="Game over!"
            GameOver(code, "start()") 
        
        if (self.avtank<MIN_GAS_BEFORE_DIE):
            self.engine=0
            self.avtank=0
            GAMERUNNING=0
            code="[Gas]" 
            GameOver(code, "start()")
        
        if (self.avtank >0):
            self.engine=1
            GAMERUNNING=1
            code="OK"        
        
        return code
#_____________________________________________________________________________________________

    def stop(self):
        # Called when Engine OFF is pressed (O) by user
        code=""
        
        if not GAMERUNNING:
            code="Game over!"
            GameOver(code, "stop()") 
        
        if self.engine >0: 
            self.engine=0 
            code="OK"
        else:
            code="Engine is already OFF!"
                
        return code

#_____________________________________________________________________________________________
    
    def plot(self): # called from step() at every loop iteration
        """
        xn,yn lists are populated for x-axis and y-axis values (e.g. self.drivetime, self.speed) by step() ONLY while there's gas, and engine is ON.
        The arrays are already defined globally in main driver.        
        
        """
        if (DEBUG==2): print("x1 list:", x1, "y1 list:", y1) # debug (plotting coordinates)
        
        import matplotlib.pyplot as plt
               
        # Create a grid for 4 plots in a grid using subplot()--- 2x2
        # Plot 1: travel time (x) vs speed (y)
        plt.subplot(2,3,1)
        plt.plot(x1,y1, color='#B0C4DE', marker='o', linewidth=1, markersize=3)
        plt.title("1. Speed @ Specific Time", fontsize=12, color='#B0C4DE')
        plt.xlabel("speed (mph)", fontsize=9, color='#B0C4DE')
        plt.ylabel("time (hr)", fontsize=9, color='#B0C4DE')
        plt.tick_params(axis='both', which='major', labelsize=8)

        # Plot 2: speed (x) vs avaiable gas (y)
        plt.subplot(2,3,2) 
        plt.plot(x2,y2, color='#778899', marker='o', linewidth=1, markersize=3) 
        plt.title("2. Speed vs Available Gas", fontsize=12, color='#778899')
        plt.xlabel("speed (mph)", fontsize=9, color='#778899')
        plt.ylabel("available gas (gal)", fontsize=9, color='#778899')
        plt.tick_params(axis='both', which='major', labelsize=8)

        # Plot 3: Miles traveled (x) vs avaiable gas (y)
        plt.subplot(2,3,3)
        plt.plot(x3,y3, color='#87CEFA', marker='o', linewidth=1, markersize=3) 
        plt.title("3. Distance vs Available Gas", fontsize=12, color='#87CEFA')
        plt.xlabel("traveled (miles)", fontsize=9, color='#87CEFA')
        plt.ylabel("available gas (gal)", fontsize=9, color='#87CEFA')
        plt.tick_params(axis='both', which='major', labelsize=8)

        # Plot 4: Miles traveled (x) vs Speed (y)
        plt.subplot(2,3,4) 
        plt.plot(x4,y4, color='#5F9EA0', marker='o', linewidth=1, markersize=3)
        plt.title("4. Speed vs Distance", fontsize=12, color='#5F9EA0')
        plt.xlabel("speed (mph)", fontsize=9, color='#5F9EA0')
        plt.ylabel("traveled (miles)", fontsize=9, color='#5F9EA0')        
        plt.tick_params(axis='both', which='major', labelsize=8)

        # Plot 5: Speed (x) vs MPG (y)
        plt.subplot(2,3,6) 
        plt.plot(x5,y5, color='#6495ED', marker='o', linewidth=1, markersize=3)
        plt.title("5. Average Speed vs MPG", fontsize=12, color='#6495ED')
        plt.xlabel("avg. speed (mph)", fontsize=9, color='#6495ED')
        plt.ylabel("gas performance (mpg)", fontsize=9, color='#6495ED')
        plt.tick_params(axis='both', which='major', labelsize=8)

        plt.show() 

        return

#_____________________________________________________________________________________________        

"""
==============================================================================================
"""

def GameOver(s, caller):
    # called when GAMERUNNING = 0   
    print('\033[37;41;1m')
    print("GAME OVER! Thank you for playing. [Exit code:", s, "]")
    ShowStats() 
    
    print('\033[39;49m')
    
    if s!="User quit game":
        print('\033[33;40;1m') 
        print("\n===>Check the pop-up window titled 'Figure 1' for analytics.\n")
        print('\033[39;49m') 
        if (DEBUG): print("\tCaller fn:", caller) # debug
        if (DEBUG): print("\t.avtank:", my_car.avtank) # debug
        my_car.plot()
    
    sys.exit()

#____________________________________________________________________________________
def ShowStats():
    # called when Stats (T) or (C) is pressed and when game is over (GAMERUNNING)
    print('\033[34;47;1m') 
    
    print("\r\n[STATS] *** Current Speed: {} mph; Odometer (traveled):{} miles; Fuel Avail.:{} gal; Fuel Used (to-date):{} | Overall Avg Speed:{} mph; Drive Time: {} hrs; Latest MPG:{} ***\r\n"\
                  .format(my_car.speed, my_car.odometer, my_car.avtank, round(my_car.usedgas,0), my_car.average_speed(), my_car.drivetime, my_car.mpg))
    
    
    print('\033[39;49m')

    return

#____________________________________________________________________________________

####### main driver #########
import sys 

import os  
os.system("")

if __name__ == '__main__':                            
    x1=[] 
    y1=[] 
    x2=[] 
    y2=[] 
    x3=[] 
    y3=[] 
    x4=[] 
    y4=[] 
    x5=[] 
    y5=[] 
    
    DEBUG=0 
    

    my_car = Car()
    print('\033[32;40;1m' + "I'm a car!")
    GAMERUNNING=1
    MIN_GAS_BEFORE_DIE=0.05 
   
    while GAMERUNNING:
        print('\033[37;44;1m')
        
        action = input("Give me a command-> Show car specs [I], Start [E]ngine, Turn [O]FF Engine, [A]ccelerate, [B]rake, Show S[T]atistics, [C]ontinue (next iteration), [P]lot analytics, [Q]uit: ").upper()        
        if action not in "AEOBPQITC" or len(action) < 1:
            print('\033[33;40;1m')
            print("...I don't know how to do that!...")
            print('\033[39;49m')
            
            continue 
        
        print('\033[37;45m')
        
        if action == 'A':
            print('\033[32;40;1m') 
            s=my_car.accelerate()
            print("Acceleration attempt:",s, "Current Speed:", my_car.speed)
            print('\033[39;49m') 
            
        elif action == 'E':
            r=my_car.start()
            if r=="OK":
                print('\033[32;40;1m') 
                print("...ENGINE IS RUNNING...")
                print('\033[39;49m') 
                
            else:
                print('\033[33;40;1m') 
                print("Problem starting car! Reason code:", r)
                print('\033[39;49m') 
                        
        elif action == 'O':
            r=my_car.stop()
            if r=="OK":
                print('\033[32;40;1m') 
                print("ENGINE IS OFF!")
                print('\033[39;49m') 
            else:
                print('\033[33;40;1m') 
                print("Warning code:", r)
                print('\033[39;49m') 

        elif action == 'B':            
            s=my_car.brake()
            print('\033[32;40;1m') 
            print("Deceleration attempt:",s, "Current Speed:", my_car.speed)
            print('\033[39;49m') 
                            
        elif action == 'P':            
            my_car.plot()            
            continue 

        elif action == 'Q':
            GAMERUNNING=0            
            GameOver("User quit game", "main()") 
            

        elif action =='I':
            print("\r\n[SPECS] *** My top speed:{} MPH; Tank capacity:{} Gal (~2gal reserve); Optimal Gas Perf.:{} MPG; Range: {} Miles | \
Acceleration: {} miles/command; Deceleration: {} miles/command\r\nOptimal gas usage: {}-{} MPH ***\r\n"\
.format(my_car.topspeed, my_car.maxtank, my_car.mpg, my_car.range, my_car.acceleration, my_car.deceleration, my_car.optimalmpg[0], my_car.optimalmpg[1]))
            continue  

        elif action =='T': 
            ShowStats() 
            continue
            
        elif action =='C': # difference between 'T' and this is that this updates time and all stats (as continuing at current speed), where T only shows stats without affecting anything.            
            # WARNING: don't call continue here because we want the my_car.step() to run after user-actions.
            pass 

        my_car.step() 
        ShowStats() 


####### end main driver ########

