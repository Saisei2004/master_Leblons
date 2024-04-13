[日本語](./cml_ja.md) | [English](./cml_en.md)

# Carry My Luggage (CML) Challenge

## Overview
The Carry My Luggage (CML) challenge is designed to test robotic skills in a practical scenario where a robot assists in carrying luggage to a car parked outside from inside a known environment, and autonomously returns to the starting point. This challenge focuses on manipulation, navigation, human-robot interaction, and object recognition.

## Reference Video
[Watch the reference video here](https://youtu.be/dzyJ1dHTulc)
> **Note:** This video is for guideline purposes only. Please note that the rules may vary each year.

## Objectives
The main objective for the robot is to assist in carrying luggage from a known environment to an unknown environment where the vehicle is parked and return back to the starting point autonomously.

## Environment Setup
- **Location:** The competition is set in a home-like arena, including activities both inside and outside of this area.
- **Start Location:** Robots start from the center of the Dining Room facing two chairs.
- **Luggage (Paper Bags):**
  - Location: Near the operator, visible within 2 meters of the robot.
  - Details regarding size and specific placement to be confirmed on the competition day.
- **Operator:** Will stand in front of the robot and indicate which bag to use.

## Competition Phases
### Start Phase
1. **Duration:** Total competition time is 7 minutes.
2. **Initiation:** Robots are placed at the start location by the teams.
3. **Commencement:** The referee signals the start of the competition.
4. **Bag Identification:** The operator points to the bag to be used, which the robot then identifies and grasps.

### Follow-Me Phase
1. **Transport Initiation:** The robot signals readiness to follow the operator.
2. **Traversal:** The operator leads the robot from the known to the unknown environment.
3. **Tracking:** The robot follows the operator to a designated goal outside the arena.

### Navigation Phase
1. **Bag Handover:** The operator receives the bag from the robot and expresses gratitude.
2. **Return Trip:** The robot autonomously navigates back to the starting point, avoiding any preset obstacles.

## Scoring
### Main Goals
| Action                                 | Score |
| -------------------------------------- | -----:|
| Picking up the correct bag             |   100 |
| Following the operator to the car      |   300 |
| Avoiding predefined obstacles          | Varies |

### Bonus Points
| Action                     | Score |
| -------------------------- | -----:|
| Successfully re-entering the arena |   100 |

### Penalties
| Action                             | Score |
| ---------------------------------- | -----:|
| Dropping the bag                   |   -50 |
| Deus Ex Machina interventions      | -50 to -200 |

## Rules and Regulations
Changes to the rules can happen, and participants are advised to check [GitHub Issues](https://github.com/RoboCupAtHomeJP/Rule2023/issues) for real-time updates and discussions.

## Contribution
Teams are encouraged to provide feedback and participate in the ongoing development of the competition rules by submitting issues and pull requests to this repository.

