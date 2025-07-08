from qai_hub_models.models import llama_v3_8b_instruct

model = llama_v3_8b_instruct.get_model()

prompt = "What is the capital of France?"
response = model(prompt)
print(response)
