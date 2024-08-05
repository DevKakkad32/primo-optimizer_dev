Project Efficiency Score Calculation
====================================

Typical Efficiency Factor
-------------------------
PRIMO allows users to customize the definition of high-efficiency projects. Users are required to provide PRIMO 
with efficiency factors they wish to implement, along with corresponding weights for each factor. Some typical 
efficiency factors include:

- Number of wells
- Number of unique owners
- Distance to centroid [miles]
- Average distance to road [miles]
- Average elevation delta [m]
- Age range [years]
- Average age [years]
- Depth range [ft]
- Average depth [ft]
- ...

Calculate Efficiency Score of Projects
--------------------------------------
The efficiency score of a project is determined based on information associated with designated efficiency 
factors for the scenario. Scores are normalized to a scale of 0 to 100 using the minimum and maximum values of 
the corresponding data.

**Step 1: Identify the maximum and minimum values of data associated with efficiency factors**

*Project-specific factors*

For factors where values depend on the entire project (e.g., number of wells, number of unique owners), the maximum 
values among all selected projects are used. The minimum values are set to correspond to the scenario of a 
single-well project.

*Well-specific factors*

For factors dependent on individual wells in the project (e.g., age range, average elevation delta), the maximum 
and minimum values among all wells (both selected and unselected) are used.


**Step 2: Process data associated with well-specific efficiency factors**

For efficiency factors requiring well-specific information within projects, data from all wells must be 
processed to derive project-level values. For instance, the average depth of the project is computed by averaging
the depths of all wells included. The age range is determined by calculating the difference between the oldest and 
youngest wells in the project.


**Step 3: Calculate scores associated with each efficiency factor for the projects**

Depending on the user's definition of high-efficiency projects, efficiency scores are calculated in different ways:

*Prefer larger values*

For factors where larger values indicate higher efficiency, such as desiring more wells in a project, the 
efficiency score is calculated using the equation :eq:`eq:eff1`:

.. math::
  :label: eq:eff1

  \textcolor{brown}{v^e} = \textcolor{brown}{m^e} \times \frac {(\textcolor{brown}{b} - \textcolor{brown}{b_{min}})} {(\textcolor{brown}{b_{max}} - \textcolor{brown}{b_{min}})}

*Prefer smaller values*

For factors where smaller values indicate higher efficiency, such as desiring less divergence in the age of wells 
in a project (smaller age range), the efficiency score is calculated using the equation :eq:`eq:eff2`:

.. math::
    :label: eq:eff2

    \textcolor{brown}{v^e} = \textcolor{brown}{m^e} \times \frac {(\textcolor{brown}{b_{max}} - \textcolor{brown}{b})} {(\textcolor{brown}{b_{max}} - \textcolor{brown}{b_{min}})}


.. list-table:: **Parameters**
        :widths: 25 75
        :header-rows: 1

        * - Symbol
          - Description
        * - :math:`\textcolor{brown}{b}`
          - The original data associated with the efficiency factor of a project
        * - :math:`\textcolor{brown}{b_{max}}`
          - The maximum data associated with the efficiency factor
        * - :math:`\textcolor{brown}{b_{min}}`
          - The minimum data associated with the efficiency factor  
        * - :math:`\textcolor{brown}{m^e}`
          - The relative weight assigned with the efficiency factor
        * - :math:`\textcolor{brown}{v^e}`
          - The metric score of the efficiency factor for a project
  

**Step 4: Calculate the total efficiency score of the projects**

The total efficiency score of a project is calculated by summing all scores that the project receives under all 
efficiency factors.
