## Steps to save jobs in azure


1. Install the Azure Machine Learning Python SDK and the python-dotenv package

```bash
pip install azureml-sdk python-dotenv
```

2. Create and import secrets

- Create a .env file in the directory with your secrets

```txt
AZURE_SUBSCRIPTION_ID=XXXX
AZURE_RESOURCE_GROUP=RG-BENIAC
AZURE_WORKSPACE_NAME=cinema
```

- Import secrets

```py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
resource_group = os.getenv("AZURE_RESOURCE_GROUP")
workspace_name = os.getenv("AZURE_WORKSPACE_NAME")
```

3. Connect to workspace

```py
from azureml.core import Workspace
ws = Workspace.get(
    name=workspace_name,
    subscription_id=subscription_id,
    resource_group=resource_group
)
```


4. Create or use an experiment, create a new run

```py
from azureml.core import Experiment, Run

experiment = Experiment(workspace=ws, name="test_experiment")
```


5. Create the run and log info

```py
run = experiment.start_logging(display_name="test_run")

# Your machine learning experiment code here

# Assuming you have a variable 'accuracy' that holds your model's accuracy
run.log("Accuracy", 0.8)

# Assuming 'model' is your trained machine learning model
#run.upload_file("model.pkl", path_or_stream="path_to_your_model.pkl")

run.complete()
```