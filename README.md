# Robocar_control_app
Control application in Robocar project

# Main project
More information on the project available at:
https://github.com/juanma-rm/Robocar_SWP

# Usage
* Last connection: if the timeout (250 ms) expires before receiving information from the car, the GUI gets blocked.
* Control: allows sending commands to the car.
  * Stop mode: the engines stop.
  * Manual mode: the user can select the percentage of speed in both straight and side directions, being positive values for forward (straight) or right (side) and negative values for backward (straight) or left (side) directions. For instance: 
    * {OY=100%, OX=0%} results in going straight forward at maximum speed
    * {OY=-100%, OX=0%} results in going straight backward at maximum speed
    * {OY=100%, OX=100%} results in turning right on site
    * {OY=100%, OX=-100%} results in turning left on site
    * {OY=100%, OX=50%} results in going straigth forward slowing down right motor to 50% of the straight speed (therefore, turning right slightly).
  * Automatic mode: lineal speed setpoint for automatic control PID-based control. Not implemented yet in Main Control System.
* Telemetry: shows information about the last status received from the car (workmode, last command received, current speed, current distance detected by ultrasonics sensors).

Screenshot:\
![Telemetry_System_GUI_v2](https://user-images.githubusercontent.com/41286765/168443228-a6664ea9-1649-4e20-b862-bcf5f9023c54.png)


# Contact <a name="Contact"></a>

[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- MARKDOWN LINKS & IMAGES -->

[linkedin-shield]: https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white
[linkedin-url]: https://www.linkedin.com/in/juan-manuel-reina-mu%C3%B1oz-56329b130/
