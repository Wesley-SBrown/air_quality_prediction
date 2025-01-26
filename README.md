## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/Wesley-SBrown/air_quality_prediction.git
    cd air_quality_prediction
2.  Create a virtual environment and install dependencies:
    ```bash
    python3.12 -m venv venv
    source venv/bin/activate   # For Linux/Mac
    .\venv\Scripts\activate    # For Windows
    pip install -r requirements.txt

* Make Sure to install the requirements txt file whilst inside the environment ( you can comment out undesired modules )



## Specific Branch Role
Analysis Done by Max Vo on the EPA air quality dataset

[Endpoints](https://aqs.epa.gov/aqsweb/documents/data_api.html#quarterly) | 
[Specifications](https://aqs.epa.gov/aqsweb/documents/aqs_api_specification.json) | [Parameters](https://aqs.epa.gov/aqsweb/documents/codetables/parameters.html) | 
[Codes](https://www.epa.gov/aqs/aqs-code-list) | [Criteria Pollutants](https://aqs.epa.gov/aqsweb/documents/codetables/methods_criteria.html)
* __PM2.5__ Particulate Matter with a diameter of 2.5 micrometers or smaller: can penetrate deeper into the respiratory system compared to PM10.
* __LC__ ( Liquid Chromatography): The analytical method used to measure concentrations in PM2.5 particles.
* __TOT__ (Thermal-Optical Transmittance): "A widely used analytical method for measuring carbonaceous aerosol concentrations. TOT differentiates between organic carbon (OC) and elemental carbon (EC) by heating the sample and measuring the light transmittance through the filter"
* __STP__ (Standard Temperature and Pressure): reference condition commonly used in environmental and scientific measurements to ensure consistency across different datasets
  * Temperature: 0°C (273.15 K)
  * Pressure: 1 atmosphere (101.325 kPa)



