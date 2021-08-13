# 2021_intern_code_data
## 
author: Yamei Tu(tu.253@osu.edu)

## Data
* the data is saved in the following link: https://ibm.box.com/s/7pqic3v1hb24hmvpa6elzatvxmrfna80
* if you want to run the system, download the data, and put Data/ and Code/ in the same parent folder(this step will not need in the near future, only XAI_log_embedding/ is required).

### Data/
```
📦Data
 ┣ 📂Raw Data (raw log data collected by Kevin)
 ┃ ┣ 📂2abnormal_data
 ┃ ┃ ┣ 📂network_latency_cpu_hog
 ┃ ┃ ┣ 📂network_loss_memory_hog
 ┃ ┣ 📂high_severe (three types of high severe)
 ┃ ┃ ┣ 📂network_corruption
 ┃ ┃ ┣ 📂network_latency
 ┃ ┃ ┣ 📂network_loss
 ┃ ┣ 📂low_severe
 ┃ ┃ ┣ 📂cpu_hog_carts
 ┃ ┃ ┣ 📂memory_hog
 ┃ ┃ ┣ 📂pod_deletion
 ┃ ┣ 📂normal_data(normal data for training the model-automation, and some sampling data from it)
 ┃ ┣ 📂test_data(model-automation is trained on normal_data, and test on test_data)
 ┣ 📂XAI (pre-processing steps for generating data for XAI_Log_embedding/ interface)
 ┃ ┣ 📂2_abnormal (run LDA on the log data when we injecting two faults at the same time, and collect the intermediate result and final prediction) 
 ┃ ┃ ┣ 📂log_level
 ┃ ┃ ┣ 📂window_level
 ┃ ┣ 📂baseline (baseline model related data) 
 ┃ ┣ 📂carts
 ┃ ┃ ┣ 📂embeddings
 ┃ ┃ ┃ ┣ 📂log_level (zeno_preprocessing processed log line) 
 ┃ ┃ ┃ ┣ 📂window_level(zeno_preprocessing processed windows, and predictions from LAD) 
 ┃ ┣ 📂compare_tem_embed (compare result from template, and embedding template) 
 ┃ ┃ ┣ 📂occurrence
 ┃ ┣ 📂lime (lime algorithm related data) 
 ┃ ┣ 📂normal (similar with carts/embeddings, but for normal data) 
 ┃ ┃ ┣ 📂log_level
 ┃ ┃ ┣ 📂window_level
 ┃ ┣ 📂pre_zeno (prediction + zeno-preprocessing )
 ┃ ┣ 📂pre_zeno_logline (pre_zeno + related log lines (retrieved by the timestamp start/end))
 ┃ ┣ 📂pre_zeno_logline_temid (pre_zeno_logline + adding related template id to the log lines ) 
 ┣ 📂gui (data used in the interactive system ) 
 ┣ 📂sysdig
 ┃ ┣ 📂combined (combined metrics info for each fault)
 ┃ ┣ 📂cpu_hog
 ┃ ┣ 📂memory_hog
 ┃ ┣ 📂network_corruption
 ┃ ┣ 📂network_latency
 ┃ ┣ 📂network_loss
 ┃ ┣ 📂normal_3_5
 ┃ ┣ 📂normal_5_6
 ┃ ┣ 📂raw_sysdig_data
 ┃ ┃ ┣ 📂cpu_hog
 ┃ ┃ ┣ 📂memory_hog
 ┃ ┃ ┣ 📂network_corruption
 ┃ ┃ ┣ 📂network_latency
 ┃ ┃ ┣ 📂network_loss
 ┃ ┃ ┣ 📂normal_half_1
 ┃ ┃ ┣ 📂normal_half_2
 ┃ ┣ 📂train (training data for classification based on combined) 
 ┣ 📂train_data (classification on log data) 
 ┃ ┣ 📂train_0607
 ┃ ┣ 📂train_model (trained model using model-automation pipeline on [sockshop_2020-09-29_to_10-07_sorted.json](https://ibm.ent.box.com/folder/142587993475))
 ┃ ┣ 📂output
 ┃ ┃ ┣ 📂carts
 ┃ ┃ ┣ 📂carts-db
 ┃ ┃ ┣ 📂catalogue
 ┃ ┃ ┣ 📂front-end
 ┃ ┃ ┣ 📂orders
 ┃ ┃ ┣ 📂orders-db
 ┃ ┃ ┣ 📂payment
 ┃ ┃ ┣ 📂queue-master
 ┃ ┃ ┣ 📂shipping
 ┃ ┃ ┣ 📂user
 ┃ ┃ ┣ 📂user-db
```
## Introduction to file 
* lime.ipynb: run LIME algorithm
* sysdig.ipynb: run classification on the sysdig data
* xai3.py: pre-processing data for XAI interface
* XAI_log_embedding: codes for the visual interactive system  
![image](https://github.ibm.com/Yamei-Tu/2021_intern_code_data/blob/master/Code/XAI_screenshot.png)

## How to run the system?
0. Code: please pull the most updated version https://github.com/yasmineTYM/XAI_log_embedding.git
[currently the code and data are seperate, i will move the necessary data into the code folder in the future]

1. Open Virtual Environment 
* cd XAI_log_embedding/gui/
* source /env/bin/activate
* pip install Flask==1.0.2 Flask-Cors==3.0.7

2. Run Backend
* cd XAI_log_embedding/gui/server
* python app.py 
* it should show:
![image](https://github.ibm.com/Yamei-Tu/2021_intern_code_data/blob/master/Code/backend.png)

3. Install Front-end packages 
* cd gui/frontend/
* remove node_modules/ 
* remove package-lock.json
* npm cache clean --force
* npm install 
* npm install --save vuex

4. Run front-end
* cd gui/frontend/
* npm run dev
* if face error: ELIFECYCLE errno 1 failed at the ~, try to run: unset HOST and try it again. 

5. All the data used in the system is saved in the Data/gui/

## Explain how we generate the data for the system. 
1. Run the pipeline of Log Anomaly Detector 


2. Collect the following raw data
- [zeno-preprocessing], collect four files under the temp/: 
  - normal-template.txt, 
  - normal-windowed.txt, 
  - abnormal-template.txt, 
  - abnormal-windowed.txt
- [log-anomaly-detector], collect two files under the eval_output/:
 - pre_anomaly_windowed-logs.json
 - pre_anomaly_normal-windowed-logs.json
- [log-anomaly-detector], collect two files under the root:
 - abnormal-windowed-logs.json
 - normal-windowed-logs.json
 - uncertain-windowed-logs.json
 
 3. run **pre_zeno()** in xai3.py, read pre_anomaly_windowed-logs.json, append addtional embedding information from normal-windowed.txt and abnormal-windowed.txt, saved in Data/XAI/pre_zeno. 
 
 4. run **pre_zeno_logling()** in xai3.py, get related log embeddings. 
 
 5. run **addTemplateId()** in xai3.py, append the template id for the related logs. 
 
 6. run **TreeData()** in xai3.py, compare the prediction with the original ground truth, which is used for the timeline visualization 
 
 7. run **combineAll()** in xai3.py to get the template for all log embeddings(contain normal and abnormal), saved in XAI/baseline/log
 
 8. run **trainData1()** in xai3.py, combine the normal and abnormal logs, prepare the training data for LIME. 
 
 9. run lime.ipynb.to generate LIME result.
 
 10. run addLime() in xai3.py, 
 
 
