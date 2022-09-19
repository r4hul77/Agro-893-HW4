# Agro-893-HW4

**Homework 4**          AGRON 893 – Fall 2022 *Due: 23 Sep 22* 

**NOTE**: This assignment is to be worked by the entire class working as one team.  You only need to turn in one copy, which can be emailed to the instructor. ![](Aspose.Words.c0317689-50ca-4a0c-98e6-61624fffc7a5.001.png)

Problems 

(100 points)  Complete and fully test the  Cars\_and\_UAVs.py program.  You need to simulate four trips, two with a Car and two with a UAV.  Among the Car trips, one should be doable with one tank of petrol but the other should take several.  For the UAV missions, one should take less than a full battery charge but the other should exceed the battery capacity.  There are several tasks to accomplish: 

1. Study and understand the current code. 
1. It has been said that “The only sane attitude one can take toward computer code is paranoid suspicion”.  The code accompanying this assignment does simulate a single-tank trip without failing.  However, you *should not* assume that it is working correctly – you need to confirm that the right answer is being obtained. 
1. When computing the Car’s speed and efficiency during the trip, the code does not do so as a function of position.  Notes in the code show where this programming is to be placed. 
1. Research has to be done to find out how to compute energy use by UAVs and coding generated.  There are various online-calculators and websites with relevant information.  Electrical units need to be converted to the units used by the Vehicle superclass.  The current values used to create drones are complete *ad hoc* and must be replaced by realistic ones. 
1. Code is needed in the main() to be written to plan and fly UAV missions analogous to the Car trips.   
1. Testing, testing, testing to ***prove*** the correct answers are being computed. 
1. Because the integration is conducted solely in the Superclass, you could, optionally, at your choice, modify the code let you to capture and graph position as a function of time and then have a method that can will plot the results if/when the trip ends.  

You should divide these tasks as it seems best to you.  Relative to programming, you might want to have more than one version undergoing parallel development by different (sets of) people.  Different versions will have different errors, suggesting multiple lines of attack and/or work arounds that can be shared and synthesized.  Your time is short so you want to avoid task assignment schemes where everybody ends up waiting on a few people. Organize your operation so as to maximize parallelism. 

And ask lots of questions of each other and your instructor.  Do so in ways that rapidly get the flows of answers to as many people as possible in as short a time as possible.  
