# ClassCar
This program is built with an object-oriented design from the ground up in Python. It’s a game or simulation if you will, but has all the plumbing necessary to make it fancier, and a 2D or even a 3D game. It works as follows:
You create a car object. Then control it (turn on or off the engine, accelerate, decelerate/brake), as well as real-time graph analytics and status. You can also check the specs of the car any time, which is built of the parent class…it determines its expected MPG, top speed, gas tank, and other properties. The objective is to see how different parameters are affected over time due to velocity and such.

For example:

How many miles can you eek out with a full tank? (speed is a factor)
What’s the longest travel time you can achieve? (gas is a factor)
What’s the best average MPG you can get and how far did you travel with that average MPG?
The MPG (miles per gallon) is calculated at real-time, at every iteration. Each iteration is a simulated 1 hour. The gas used is calculated based on your velocity and running MPG, and of course, the odometer (miles traveled). The car’s optimal gas performance is when it’s at between 30 MPH (miles per hour) and 60 MPH. If slower than 30, or faster than 60, the gas usage increases by 10% of normal burn. It’s possible to get down to 0 MPH while you still have gas, by applying brake. Each acceleration increases velocity by 20 MPH, while each braking slows it down by 25 MPH…by manipulating these you can reach speeds in other increments than just 20. The maximum tank is at 20 gallons at the start of the game. There’s no refueling. The game continues as long as there’s gas. Note that when you’re car is idling (speed=0, but engine is ON), you’ll be using gas still.

At the end of each interation (when you accelerate (A), decelerate (B), continues (C), start engine (E), turn off engine (O)), the time is updated (increases by 1 hour) along with all key parameters such as travel time, travel distance, gas usage, etc. However, informational commands such as ‘Show car specs (I)’, ‘Show Statistics (T)’, Plot analytics (P) will just show the requested information without affecting time, speed, gas etc…it’s like a live Pause. Whereas, Continue (C) will update but will keep the speed exactly as you left in previous interation (that is, no need to accelerate or decelerate to get to next iteration).

Besides the object-oriented design, there are a couple of cool things going on here. One of them is the obvious color-coding of this text-based game without using any special library…just by using ANSI sequences. For example, ESCAPE sequence ESC[32 would turn the foreground text to green. There is a bunch of these sequences you can look up online, I use some of them and combine a few to change the foreground and background colors at the same time, including brightness. For example, print(‘\033[32;40;1m’) would result in green text on black bg in the next print() statement.

The second cool part is the real-time plots using matplotlib library. I create 5 plots in a single window showing various metrics of the session. You can view plot anytime by pressing P and it’ll open the plots in a new window…to get back to the game prompt, close the plot window. At the end game, it’ll also show you the plot also (exception: When you Quit, there’s no plot, game is terminated immediately without any delay).

When game exits (when you’re out of gas), the UI will show the final stats and a reminder to check the plots.

As mentioned above some of the things to look for:
  How many miles can you eek out with a full tank? (speed is a factor)
  What’s the longest travel time you can achieve? (gas is a factor)
  What’s the best average MPG you can get and how far did you travel with that average MPG?
  And more
 
 A bit more about the design:

The Car class is defined as follows:
  class Car:
  def init(self, speed=0):
  self.speed = speed
  self.odometer = 0
  self.drivetime = 0
  self.maxtank = 20.0 # Fixed property
  self.mpg = 40.0
  self.topspeed = 100 # Fixed property
  self.engine=0
  self.avtank=self.maxtank
  self.usedgas=0
  self.range=round(self.maxtank * self.mpg, 3)
  self.acceleration = 20 # Fixed property
  self.deceleration = 25 # Fixed property
  self.optimalmpg=(30,60) # Fixed property

There are several methods in that class:
  get_curr_speed(self) # returns current speed.
  accelerate(self) # this increases velocity by self.acceleration value.
  brake(self) # reduces velocity by self.deceleration.
  step(self) # this is crux of the math behind the game. Updates all inter-dependent parameters such as time, odometer, gas availability, average MPG, checking condition to exit or not, etc. And it populates all the data points required to plot all 5 graphs in their respective lists. It also handles showing car specifications on demand to user.
  average_speed(self) # this calculates the running average speed and return that value.
  start(self) # this starts the engine and makes sure all conditions for start is met and returns a code accordingly.
  stop(self) # this turns off the engine making sure all conditions are stop are met, etc. Also returns a code.
  plot(self) # This does the actual plotting on screen of all graphs using the data points that are updated in step() method.

The game has other functions outside of the class for the general control of the flow of the application such as:
GameOver(message, exit_code) # this will quit the app with specific message and code depending on the condition.
ShowStats() # this will show latest key statistics

For efficiency, I don’t populate the lists of datapoints unless the car is moving or has moved at least once. Additionally, when the same scales are used in more than one plot (e.g. speed (mph) data points), I don’t copy the entire list of datapoints again, instead, I point to the same list in memory and pluck the datapoints from there. This reduces the memory usage and just results in overall faster execution.

For more and EXE download, see http://flyingsalmon.net/?p=3444
