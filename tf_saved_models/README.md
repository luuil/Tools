## Usage

1. Put frozen models into `./frozen` directory
2. Add serving information in `export_serving_model.py`
    - Define a export function
    - Put `@ServingInfo.export` decorator on export function(**if not, then this model will not export**)
3. Run `export_serving_model.py`
4. Copy the serving model `./serving/{version}` to your serving model directory on the server

## Test

You don't need to konwn what the `hyaudio` model is. We just use it
to demonstrate the export functionality.

We will export the same model two times to simulate the simultaneous
export multiple models.

When you export multiple models, you should specify the

- `signature_name` 
- `input_signature_map`
- `output_signature_map` 

parameters. They refer to **signature for serving**, **entry point of the model**
and **output point of the model** respectively. 


| model | signature_name | input_signature_map | output_signature_map | frozen location(`./frozen`) |
|----------------|---------------------|----------------------|-----------|------|
| [model description]  | hyaudio_1  | `'inputs':'hyaudio/vggish_input:0'` | `'classes':'hyaudio/predict_classes:0', 'probs':'hyaudio/predict_probs:0'` | `audio/hyaudio.pb` |
| [model description]  | hyaudio_2  | `'inputs':'hyaudio/vggish_input:0'` | `'classes':'hyaudio/predict_classes:0', 'probs':'hyaudio/predict_probs:0'` | `audio/hyaudio.pb` |

## Check the serving model

We use the [SavedModel CLI][saved_model_cli] tool to check our exported models.

To show all available SignatureDef keys in a MetaGraphDef.

```bash
saved_model_cli show --dir ./serving/1 --tag_set serve
```

To show all inputs and outputs TensorInfo for a specific SignatureDef, pass in the SignatureDef key to signature_def option. This is very useful when you want to know the tensor key value, dtype and shape of the input tensors for executing the computation graph later.

```bash
saved_model_cli show --dir ./serving/1 --tag_set serve --signature_def hyaudio_1
```

[deploy_tf]: http://172.28.84.27/doku.php?id=http_service:deploy_tf
[saved_model_cli]: https://www.tensorflow.org/versions/r1.2/programmers_guide/saved_model_cli