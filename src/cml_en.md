[日本語](./cml_ja.md) | [English](./cml_en.md)

Carry My Luggage (CML)
Reference video: https://youtu.be/dzyJ1dHTulc

Note
The reference video is not perfect. The rules may vary by year, so please refer to it only as a guideline.
If you have any concerns or points of discussion, please submit them to the GitHub Issues.

Main Goal
In this task, the robot assists the operator in carrying luggage to a car parked outside. After grabbing the luggage (paper bags), the robot follows the operator from a known to an unknown environment, assisting in luggage transport, and then autonomously returns to the starting point (known environment).

Focus
This task focuses on pointing recognition, manipulation, mapping and navigation in known and unknown environments, following human movements, voice interaction, and task planning.

Setup
Location: The competition uses a home-like arena environment, conducted both inside and outside the arena. The inside of the arena can be mapped in advance (known environment).

Start Location: The robot starts from the center of the Dining Room, facing towards the center between two chairs.

Luggage (Paper Bags): Two paper bags are placed near the operator (within 2
�
m and visible to the robot).

Size: To be determined
Placement: This will be done by the OC and TC. The bags will be placed on top of a chair.
Operator: The operator, who will be standing in front of the robot, will point to the paper bag to be used during the competition. The operator can be anyone from your own team.

Warning
Rules may change. This will be shared with everyone if it happens.

Scenario
Start Phase
Competition Time: The competition lasts 7 minutes.
Setup: The referee instructs the team to move the robot to the start position.
Start: The referee gives the start signal and starts the timer. At the same time, the team completes any last-minute setup (such as pressing the start button) and leaves the area. Do not perform complex setup procedures like pressing multiple buttons.
Pointing: Upon the start signal, the operator points to one of the two paper bags, previously designated.
Grasping: The robot recognizes the bag pointed out by the operator and grasps it.
Follow-Me Phase
Transportation Start: Once the robot has grasped the paper bag and is ready to follow, it communicates this to the operator.
Walking: Then, the operator starts walking from the known environment to the unknown environment. The goal location outside the arena is fixed.
Follow-Me: The robot follows the walking operator and continues to track them. Once the operator reaches the goal, they communicate this to the robot.
Warning
The operator must not turn towards the robot or stop walking once they have started.

Navigation Phase
Handover: After reaching the goal with the operator, the operator takes the bag from the robot and thanks it.
Navigation: The robot autonomously moves from the unknown environment back to the starting point in the known environment, navigating around various obstacles. Whether to tackle these obstacles is up to each team (points are added for each avoided obstacle).
The types of obstacles include:
A crowd of two people standing in the way
Small objects on the ground (such as blocks)
Difficult-to-see 3D objects (such as chairs or glasses)
Retractable barriers (such as guide poles)
Goal: Once the robot returns to the starting point, the task is completed.
Local Rules
Competition time is 7 minutes
There will be three referees, each team contributing one after their competition
Bonus tasks
No points are awarded if a retractable barrier's foot is stepped on
The range of the "starting point" is within a 50cm radius of the marked spot on the ground (effective if even partially within the range)
"Re-entry into the arena" is valid if the entire robot enters the arena
Do not place the bag vertically
Skipping of bag grasping and obstacle avoidance is permitted
Main Goals
Action	Score
Picking up the correct bag (skip rule)	100
Following a person to the car	300
Avoiding small objects on the ground (skip rule)	50
Avoiding difficult-to-see objects (skip rule)	50
Avoiding areas blocked by retractable barriers (skip rule)	50
Bonus Points
Action	Score
Re-entering the arena	100
Standard Penalties
Action	Score
Dropping the bag	50
Deus Ex Machina Penalties
Action	Score
Rediscovering the operator through natural interaction	50
Rediscovering the operator through unnatural interaction	100
Rediscovering the operator through direct contact	200
Special Penalties & Bonuses
Action	Score
Non-participation	500
Using an alternative start signal	100
Total Score: 700 points

Directions from the Executive Committee (EC)
Preparation
Select two people from the competing teams to obstruct the robot's path outdoors.
Choose the position of the paper bags and assign them to the operator.
Select the obstacles the robot will face outdoors.
Choose the position of the goal (car).
Be cautious when the robot exits the arena.
Announcements (Setup day)
Select and announce the starting point for the robot.
Choose and announce which bag will be used.
Referee (TC) Movement
Gather one person from each team that has finished competing, receive explanations, and collect the score sheets.
Act as the referee as described in the scenario.
Score the competition based on the score sheets.
Confirm the scoring details with other TCs.
Submit the score sheets.
