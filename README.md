# 2021_intern_code_data
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

In order to collect some intermediate results, some changes are required to be made:
### Changes made to the model-automation
 [src/calculate_metrics.py, in the end of **preprocess_test_data()**,](https://github.ibm.com/watson-ai4it/model-automation/blob/master/src/calculate_metrics.py#L86), add following lines:
  ```
  abnormal_data.to_json('abnormal-windowed-logs.json',orient="records",lines=True)
  
  normal_data.to_json('normal-windowed-logs.json',orient="records",lines=True)
  
  uncertain_data.to_json('uncertain-windowed-logs.json',orient="records",lines=True)
 
 ```
 ### Changes made to zeno-preprocessing
  [src/main/java/zeno/evaluation/DataPrep.java](https://github.ibm.com/watson-ai4it/zeno-preprocessing/blob/dev/src/main/java/zeno/evaluation/DataPrep.java#L161), add:
 ```
logline_output = templated_log.flatMap(new Stringifier());

logline_output.writeAsText(output_file_path1).setParallelism(1);
```
 ### changes made to model-automation
  [src/data/evaluate.py, line43](https://github.ibm.com/watson-ai4it/model-automation/blob/master/src/evaluate.py#L43), add:
 ```
     shutil.move('temp/windowed-logs/%s/%s/%s/template-logs.txt'% (APPLICATION_GROUP_ID, APPLICATION_ID, MODEL_VERSION), 'temp/windowed-logs/%s/%s/%s/normal-template-logs.txt'% (APPLICATION_GROUP_ID, APPLICATION_ID, MODEL_VERSION))
```
### changes made to log-anomaly-detector 
[app/anomaly_detector/log_anomaly_detector_facade.py](https://github.ibm.com/watson-ai4it/log-anomaly-detector/blob/dev/app/anomaly_detector/log_anomaly_detector_facade.py#L349), replaced:
```
embedding_predicted_scores, embedding_ranks, embedding_expected, embedding_prediction_errors, _ = embedding_pca_model_adapter.predict(
                    normalized_embeddings,'embedding', embedding_pca_model_adapter.feature_extractor
                )

```
[line:331](https://github.ibm.com/watson-ai4it/log-anomaly-detector/blob/dev/app/anomaly_detector/log_anomaly_detector_facade.py#L331)
```
 predicted_scores, ranks, expected_count_vector, prediction_errors, model_severity = pca_model_adapter.predict(
            dataset, 'template',pca_model_adapter.feature_extractor,
        )
```
[app/anomaly_detector/log_anomaly_detector_facade.py](https://github.ibm.com/watson-ai4it/log-anomaly-detector/blob/dev/app/anomaly_detector/log_anomaly_detector_facade.py#L405), add:
```
"embedding_expected":list(embedding_expected[idx]),
                "embedding_ranks": list(embedding_ranks[idx])
 ```
 [app/anomaly_detector/model/pca_model.py](https://github.ibm.com/watson-ai4it/log-anomaly-detector/blob/dev/app/anomaly_detector/model/pca_model.py#L77), replaced by 
 ```
   def predict(self, x_test, flag,feature_extractor=None):
      y_pred = np.zeros(x_test.shape[0])
      prediction_errors = np.zeros(x_test.shape[0])
      model_severity = self.severity
      rank_template_indices = []
      expected_count_vector = []
      for i in range(x_test.shape[0]):
          y_a = np.dot(self.proj_c, x_test[i, :]) ## projection of y onto the abnormal subspace 
          spe = np.dot(y_a, y_a) ## prediction error 
          if feature_extractor:
              x_p = x_test[i, :] - y_a ##why?
              expected_count_vector.append(feature_extractor.reconstruct(x_p,flag))
          if spe > self.threshold:
              y_pred[i] = 1 - (self.threshold / spe)
          distances = np.array([abs(d) for d in y_a])
          rank_template_indices.append((-distances).argsort())
          prediction_errors[i] = spe
      return y_pred, rank_template_indices, expected_count_vector, prediction_errors, model_severity

 ```
 [app/anomaly_detector/model/preprocess.py](https://github.ibm.com/watson-ai4it/log-anomaly-detector/blob/dev/app/anomaly_detector/model/preprocess.py#L89), replaced by:
 ```
   def reconstruct(self, x_seq,flag):
        """Computed the expected count vector from the PCA transformation

        Arguments
        ---------
            x_seq: PCA-reconstructed vector of the input count vector

        Returns
        -------
            x_new: the expected count vector from the PCA transformation
        """

        x_value = np.asarray(x_seq)

        if self.normalization == "zero-mean":
            x_value += self.mean_vec.reshape(-1)

        if self.normalization == "z-score":
            for col in range(len(x_value)):
                if self.std_vec[col]:
                    x_value[col] *= self.std_vec[col]
            x_value += self.mean_vec.reshape(-1)

        if self.term_weighting == "tf-idf":
            for col in range(len(x_value)):
                x_value[col] /= self.idf_vec[col]

        if flag=="template":
            x_new = [max(0, int(v)) for v in x_value]
            return x_new
        else:
            return x_value

        # return x_new
   ```
[app/schemas/derived_anomalies.py](https://github.ibm.com/watson-ai4it/log-anomaly-detector/blob/dev/app/schemas/derived_anomalies.py#L36), add:
```
embedding_expected: List[float]
    embedding_ranks: List[int]
 ```

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
 
 
