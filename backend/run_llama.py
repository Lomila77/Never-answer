#from qai_hub_models import get_model
#from qai_hub_models.models.registry import get_model
import qai_hub_models
help(qai_hub_models)
import qai_hub_models.models as models
dir(models)
from qai_hub_models.models import llama_v3_8b_instruct

# Explore what's available
print(dir(llama_v3_8b_instruct))

# Try calling the model if it's exposed directly
if hasattr(llama_v3_8b_instruct, "model"):
    response = llama_v3_8b_instruct.model("What is the capital of France?")
    print(response)
else:
    print("No 'model' attribute found in llama_v3_8b_instruct.")





# Load the LLaMA v3 8B Instruct model
model = get_model("llama-v3-8b-instruct")

# Run inference
response = model("What is the capital of France?")
print(response)


