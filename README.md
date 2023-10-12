# TebArf 2023 October Case Study
**Author**: Kubilay Başıbüyük  
**E-mail**: ozelolmayaneposta@gmail.com  
**Date**: 2023 Oct.

## Build procedure
* Clone the repository
* Navigate to repository and execute 
  * ``python setup.py sdist bdist_wheel``
* For local use execute
  *  ``pip install .\dist\case_study_tebarf_202310_kb-0.1-py3-none-any.whl``
* Uninstall
  * ``pip uninstall case_study_tebarf_202310_kb`` 


### Requirements
Please refer to `requirements.txt` for information on required packages

## Notes
* In the first usage program will prompt to download models. 
* Please note that only ``facebook/bart-large-mnli`` model has been tested. 
* After succesfull download program will resume its operation
* 

## Example usage
````
# Importing the library
from case_study_tebarf_202310_kb import analyze

# Initializing
# Please note that config path must be adjusted accordingly
zero_shot = analyze.ZeroShotClassification(config_file_path=r"..\config\config.ini")

# Analyzing the conversation
zero_shot.analyze_all_conversation(file_path = "..\data\simulated_conversations\prompt1_conversation1.json")
````