# Summary

- To apply methodologies in taught week to SoI 

## Elements and Methodologies

### Elements
- Requirements #reqt
- Subsystems #SS
- Design Problems
    - Design Objectives #DO
        - Targets/Constraints 
        - *Informed by #reqt* 
    - Design Variables #DV
        - Initial Ranges
        - *Informed by #physics limits*
        - *Individual #SS authority*
    - Design Enablers
        - Physical Models
        - *Mapping #DV to #DO*
 
### Methodologies
- Requirement Ranking
    - By Dependencies
        - *act A* `<<precedes>>` *act B*
        - => *#reqt A*  > *#reqt B*
      - $100
      - **Matrix Method**
- Design Space Visualisation
    - Sensitivity Analysis
    - Parallel Plots
    - Response Surfaces/Heatmapping
- Axiomatic Design
    - #DV and #DO Coupling
    - Decoupling
    - Order of priorities for design space exploration
- QFD
    - Recuesive HOQ methodology
    - Map #reqt → #DO → #DV → Derived #DV
- Objective Feasibility
    - Single-Objective Feasibility
    - Multi-Objective Feasibility
        - Multi-Objective, Multi-Variate Orthotopic Design Space
- Designing for Optimisation/Robustness
    - Heuristic Search
        - Point based solutions
        - Pareto Front Optimisation
        - Push to constraints
    - Constraint-Driven Design
        - Start with constraint
        - Push initial orthotope to constraint
        - Manipulate size and shape for design parameter weighting

## Outputs

- SysML model
    - #reqt set
        - Derived #reqt 
    - Contraint Bocks
    - Parametric Diagram
    - Recursed parametrics
- Python Scripts
    - Implemented Design Enablers
    - Design Sapce Visualisations
    - Implementation of rstool
 
