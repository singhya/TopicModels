# TopicModels
This repository contains code for NLP topic models like CORRLDA2, ECTM. These topic models are applied on hindi news articles collected frm Amar Ujala website. A brief overview of the work flow is shown below:
 
![alt text](https://github.com/singhya/TopicModels/blob/master/Workflow.jpg "ECTM model for Hindi news articles")

#### Data Pre-processing
This contains scripts to generate input files required by the ECTM system and the SVM classifier. This involves separating each article into constituent named entities and regular terms (referred to as Non-Entities).
- Used Polyglot to extract Named Entities from each article (https://github.com/aboSamoor/polyglot)

#### ECTM
Once we get data divided as entity-vocab, non-entity-vocab, entity-term-index and non-entity-term-index we run ECTM model on top of it. These input files are present in DataPreprocessing/processedData/ECTM.

#### Feature extraction 

#### ECTM
The output file from ECTM are stored under ECTM/Output. The files ECTM_theta, ECTM_psi are used to extract entity topic and word topic related features for each document. These features are stored under FeatureExtraction.

