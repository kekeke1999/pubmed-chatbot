# User Guide

Please install NodeJS, npm and Docker at first!


### 1. Data Acquisition

1. Download the all_med.txt through the link: https://drive.google.com/file/d/1U3a9nQsMu4PsD0RY6C6pD8X61A5_GgI6/view?usp=sharing and put the txt document in the directory **/data**

2. Run the **/preparation/extract_data.ipynb** to get the CSV file **all_med_data.csv**

   (If you don't want to do the steps above, you can directly use the CSV file **all_med_data.csv** we provided in the directory **/data**)

3. Run the **/preparation/data_chunk_embedding.ipynb** to get the vector **vector_data.pkl**

### 2. Initial setup for OpenSearch

1. Run the docker container with the following command using the file /app/preparation/docker-compose.yml.

   `docker-compose up`.

2. Run the **/preparation/upload_to_opensearch.ipynb** to upload the vector data to OpenSearch

3. Follow the steps below to deploy the embedding model in OpenSearch:

   1. Open the http://localhost:5601/app/dev_tools#/console to configure the OpenSearch.

   2. Send the request to configure cluster

      ```
      PUT _cluster/settings
      {
        "persistent": {
          "plugins": {
            "ml_commons": {
              "only_run_on_ml_node": "false",
              "model_access_control_enabled": "true",
              "native_memory_threshold": "99"
            }
          }
        }
      }
      ```

   3. Register a model group

      To register a model, you have the following options:

      - You can use `model_group_id` to register a model version to an existing model group.
      - If you do not use `model_group_id`, ML Commons creates a model with a new model group.

      To register a model group, send the following request:

      ```
      POST /_plugins/_ml/model_groups/_register
      {
        "name": "embedding_model_group",
        "description": "The embedding model"
      }
      ```

      

      The response contains the model group ID that you’ll use to register a model to this model group:

      ```
      {
        "model_group_id": "9hyw7owBvevNUQ9z9Kay",
        "status": "CREATED"
      }
      ```

   4. Register a local OpenSearch-provided model

      To register a remote model to the model group created in step 1, provide the model group ID from step 1 in the following request.

      Because pretrained models originate from the ML Commons model repository, you only need to provide the `name`, `version`, `model_group_id`, and `model_format` in the register API request:

      ```
      POST /_plugins/_ml/models/_register
      {
        "name": "huggingface/sentence-transformers/all-mpnet-base-v2",
        "version": "1.0.1",
        "model_group_id": "9xy57owBvevNUQ9ze6be",
        "model_format": "TORCH_SCRIPT"
      }
      ```

      

      OpenSearch returns the task ID of the register operation:

      ```
      {
        "task_id": "-By67owBvevNUQ9z4abs",
        "status": "CREATED"
      }
      ```

      

      To check the status of the operation, provide the task ID to the [Tasks API](https://opensearch.org/docs/latest/ml-commons-plugin/api/tasks-apis/get-task/#get-a-task-by-id):

      ```
      GET /_plugins/_ml/tasks/-By67owBvevNUQ9z4abs
      ```

      

      When the operation is complete, the state changes to `COMPLETED`:

      ```
      {
        "model_id": "-Ry67owBvevNUQ9z6Ka-",
        "task_type": "REGISTER_MODEL",
        "function_name": "TEXT_EMBEDDING",
        "state": "COMPLETED",
        "worker_node": [
          "08FGGIr2QuqsewTUrlwnaQ"
        ],
        "create_time": 1704812274138,
        "last_update_time": 1704812387836,
        "is_async": true
      }
      ```

      ##### Warning! Take note of the returned `model_id` because you’ll need it to deploy the model.

   5. Deploy the model

      The deploy operation reads the model’s chunks from the model index and then creates an instance of the model to load into memory. The bigger the model, the more chunks the model is split into and longer it takes for the model to load into memory.

      To deploy the registered model, provide its model ID from step 3 in the following request:

      ```
      POST /_plugins/_ml/models/-Ry67owBvevNUQ9z6Ka-/_deploy
      ```

      As in the previous step, check the status of the operation by calling the Tasks API:

      ```
      GET /_plugins/_ml/tasks/-By67owBvevNUQ9z4abs
      ```

      When the operation is complete, the state changes to `COMPLETED`

4. Add the model ID in the file  /backend/.env like below

   ```
   model_id=-Ry67owBvevNUQ9z6Ka-
   ```
   (Just an example! Please use your own model id!)
### 3. Start the Web Application

1. Run the docker container with the following command using the file /app/docker-compose.yml.

   `docker-compose up`.

2. Run the commands one by one below in your terminal

   ```
   docker network connect app_opensearch-net backend
   ```

3. Enter the directory "/app/frontend" in the terminal

    ```
   cd /frontend
   ```

4. Install dependencies

   ```
   npm install
   ```
5. Run the command to start frontend
    
   ```
   npm start
   ```
   
6. Now the application is running in the http://localhost:8080/index.html
   
Please use Chrome browser for better user experience.

Some instructions from the OpenSearch Document: https://opensearch.org/docs/latest/ml-commons-plugin/pretrained-models/