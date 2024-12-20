# Use pretrained models in OpenSearch

Most from the OpenSearch Document: [https://opensearch.org/docs/latest/ml-commons-plugin/pretrained-models/]()

### Cluster settings

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

## Step 1: Register a model group

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

## Step 2: Register a local OpenSearch-provided model

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

Take note of the returned `model_id` because you’ll need it to deploy the model.

## Step 3: Deploy the model

The deploy operation reads the model’s chunks from the model index and then creates an instance of the model to load into memory. The bigger the model, the more chunks the model is split into and longer it takes for the model to load into memory.

To deploy the registered model, provide its model ID from step 3 in the following request:

```
POST /_plugins/_ml/models/ALFC4Y0Bbv7DWZLAx3YH/_deploy
```

As in the previous step, check the status of the operation by calling the Tasks API:

```
GET /_plugins/_ml/tasks/-By67owBvevNUQ9z4abs
```

When the operation is complete, the state changes to `COMPLETED`


Warning: Each time you restart the Opensearch, you need to deploy the registered model again:
```
POST /_plugins/_ml/models/-Ry67owBvevNUQ9z6Ka-/_deploy
```

ALFC4Y0Bbv7DWZLAx3YH