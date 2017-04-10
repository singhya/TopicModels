# TopicModels
This repository contains code for NLP topic models like CORRLDA2, ECTM. These topic models are applied on hindi news articles collected frm Amar Ujala website. A brief overview of the work flow is shown below:
 
![alt text](https://github.com/singhya/TopicModels/blob/master/Workflow.jpg "ECTM model for Hindi news articles")


#### DataCollection
This repository contains java code to crawl web pages from "Amar Ujala" newspaper website. The code uses "Crawler4j" (3rd party library) and "Jsoup" library to parse "Hindi" text articles from HTML document. The text files contains news articles which are output of the crawler code and csv files contains web pages which has crawled. Each text file contains news articles based on the classes.

#### Data Pre-processing
This contains scripts to generate input files required by the ECTM system and the SVM classifier. This involves separating each article into constituent named entities and regular terms (referred to as Non-Entities).
- Used Polyglot to extract Named Entities from each article (https://github.com/aboSamoor/polyglot)
- Generated vocab-entity, vocab-non-entity files: vocabularies for all words found in dataset
- Generated term-index-entity, term-index-non-entity: replaced each article's content by solely the entity or non-entity indices found in vocabulary. These input files needed for ECTM are stored under DataPreProcessing/processedData/ectm.

-  The features used as input for Vanilla SVM are the counts of the words(Entities + regular words('Non-entities') under each document.The feature files are stored under DataPreProcessing/processedData/svm.

#### ECTM
Once we get data divided as entity-vocab, non-entity-vocab, entity-term-index and non-entity-term-index we run ECTM model on top of it. These input files are present in DataPreprocessing/processedData/ECTM. The output file from ECTM are stored under ECTM/Output.

#### Feature extraction 
##### ECTM
The files ECTM_theta, ECTM_psi are used to extract entity topic and word topic related features for each document. These features are stored under FeatureExtraction.

#### Quantitative Evaluation
##### Classification
###### SVM
This folder has python code to learn Support Vector Machine (SVM) using ECTM features. The csv files has ECTM features. This code uses sklearn and pandas inbuilt libraries in python.

###### Naive Bayes
This folder has python code for our baseline classification model - Naive Bayes. The features used are the words of the documents, excluding stop words. 

#### Qualitative Evaluation

ECTM gives us the ability to organise our news articles into a distribution over "Entity-topics", which themselves are a distributions over Word-Topics (Non-entity words). This allows us to represent a news article by the smaller defined number of entity-topic and word-topic features instead of the large number of words used to normally represent an article. These results can be found under ECTM/Output -
1. Supertopic-topics - distribution of Entity-topics over the Word-topics 
2. Top-topic entities - top K entities under each Entity-topic
3. Top-topic words - top K words under each Word-topic

Some results which clearly show the ability of ECTM to cluster entities and entity-centered word-topics. 

Some entity-topics which can be found under ECTM/Output/V2 include:
- "Banks" ~ Business
  बैंक    एसबीआई  लोन  ट्रांज़ैक्शन         देशभर        आईसीआईसीआई-बैंक        पंजाब-नेशनल-बैंक         एक्सिस ईमआई  रिजरव 
  baink esbiaaee lon  traanzaikshn  deshbhr      aaeesiaaeesiaaee-baink pnjaab-neshnl-baink   eksis eaaee  rijrv 
  bank  SBI      loan transaction   country-wide ICICI-bank             Punjab-National-Bank  AXIS   EMI   Reserve

- "Businessmen" ~ Business
  टाटा    गांधी      सायरस-मिस्तरी     टीसीएस टाटा-संस     इंफोसिस  रतन-टाटा    मिस्तरी   टाटा- ग्रुप       कालिदास
  taataa gaaandhi saayrs-mistri  tisies taataa-sns infosis rtn-taataa mistri taataa- garup kaalidaas
  TATA   Gandhi   Cyrus-Mistry   TCS    TATA-sons  Infosys Ratan-Tata Mistri Tata-Group    Kaalidas
  
- "God" ~ Spirituality
  राम   हनुमान   महात्मा     लक्ष्मण    मिशेल     तुलसीदास   सीता   विष्णु    लंका  अकबर
  raam hnumaan mhaatmaa lksmn    mishel   tulsidaas sitaa visnu  lnkaa akbr
  Ram  Hanuman Mahatma  Lakshman Michelle Tulsidas  Sita  Vishnu TCS   Akbar
  
- "Political Leaders" ~ 
  भारत    मोदी  प्रधानमंत्री-नरेंद्र-मोदी               नरेंद्र-मोदी       फोर्बेस   भारत-सरकार      जेट  पीएम-मोदी  आचार्य-बालकृष्ण ट्विटर
  bhaart modi prdhaanmntri-nrendr-modi     nrendr-modi   forbes bhaart-srkaar  jet piem-modi aachaary-baalkrisn tvitr
  Bharat Modi Prime-Minister-Narendra-Modi Narendra-Modi Forbes Bharat-Sarkaar Jet PM-Modi   Aacharya-Balakrishna Twitter
  
- "Telecom Companies" ~ Business/Technology
  रिलायंस    एयरटेल  वोडाफोन   टेलीकॉम  टराई    बीएसएनएल भारत    अनुष्का   मुकेश-अंबानी 
  rilaayns eyrtel vodaafon telikom traaee biesenel bhaart anuskaa mukesh-anbaani 
  Reliance Airtel Vodafone Telecom TRAI   BSNL     India  Anushka Mukesh-Ambani
  
- "Social Media" ~ Technology
  गूगल    भारत    फेसबुक   याहू    यूट्यूब    पेपैल   अमरीका   माइक्रोसॉफ्ट    देवदूत   विधाता 
  gaugal bhaart fesbuk   yaahu yutyub  pail   amrikaa maaikrosoft devdut vidhaataa 
  Google India  Facebook Yahoo Youtube Paypal America Microsoft   Angel  God
  
We can also see a clear relation between Entity-topics and Word-topics. For example, 

 - E[0] = "Banks" 
   Entities :
   बैंक    एसबीआई  लोन  ट्रांज़ैक्शन         देशभर        आईसीआईसीआई-बैंक        पंजाब-नेशनल-बैंक         एक्सिस ईमआई  रिजरव 
   baink esbiaaee lon  traanzaikshn  deshbhr      aaeesiaaeesiaaee-baink pnjaab-neshnl-baink   eksis eaaee  rijrv 
   bank  SBI      loan transaction   country-wide ICICI-bank             Punjab-National-Bank  AXIS   EMI   Reserve

   The Top Three word-topics for this are:
   -फीसदी    बैंक   करोड़  दर  ब्यॉज रूपये   कार्ड   कम रुपए  लाख
    fisdi   baink krode dr byoj rupye kaard km  rupe laakh
    percent bank  crore rate interest rupee xard Less rupee lakh

   -बैंकों जारी अनुसार जवाब मामले बैंक दरों पास दिन खिलाफ 
    bainkon jaari anusaar jvaab maamle baink dron paas din khilaaf
    banks released accordingly answer issue bank rates pass din against

   -सरकार साल शामिल मन्त्रालय कदम योजना क्षेत्र समस्या आम तहत 
    srkaar saal shaamil mntraaly kdm yojnaa ksetr smsyaa aam tht 
    governement years inclusion ministry steps plan area problem common under
  
   
   
   
  
