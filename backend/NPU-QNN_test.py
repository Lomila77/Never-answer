import os
import time
import logging
from qai_hub_models.models import llama_v3_8b_instruct

logging.basicConfig(level=logging.INFO)

PROMPT = "Explain the impact of climate change on global agriculture."

def check_npu_backend():
    backend = os.environ.get("QNN_SDK_ROOT") or os.environ.get("QAIRT_SDK_ROOT")
    if not backend:
        raise EnvironmentError("QNN_SDK_ROOT or QAIRT_SDK_ROOT must be set.")
    logging.info(f"NPU backend detected: {backend}")
    return backend


def load_model():
    try:
        model = llama_v3_8b_instruct.get_model()
        logging.info("Model loaded successfully.")
        return model
    except Exception as e:
        logging.error(f"Failed to load model: {e}")
        raise


def measure_inference_time(model, prompt):
    start_time = time.perf_counter()
    response = model(prompt)
    end_time = time.perf_counter()
    duration = end_time - start_time
    logging.info(f"Inference time: {duration:.2f} seconds")
    logging.info(f"Response: {response.strip()}")
    return duration, response


def main():
    logging.info("🔍 Checking NPU environment...")
    backend = check_npu_backend()

    logging.info("🚀 Loading model...")
    model = load_model()

    logging.info("🧠 Running inference...")
    duration, response = measure_inference_time(model, PROMPT)

    logging.info("✅ Done.")


if __name__ == "__main__":
    main()
