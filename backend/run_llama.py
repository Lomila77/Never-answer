import os
import sys
import logging
import argparse
from qai_hub_models.models import llama_v3_8b_instruct

logging.basicConfig(level=logging.INFO)


def check_env():
    qairt_root = os.environ.get("QAIRT_SDK_ROOT")
    qnn_root = os.environ.get("QNN_SDK_ROOT")

    if not qairt_root:
        raise EnvironmentError("QAIRT_SDK_ROOT is not set.")
    if not qnn_root:
        logging.warning("QNN_SDK_ROOT is not set. It may fallback to QAIRT_SDK_ROOT.")
    if not sys.executable or "python" not in sys.executable:
        raise EnvironmentError("Python executable not found.")
    logging.info(f"Python used: {sys.executable}")
    logging.info("Environment check passed.")


def load_model():
    try:
        model = llama_v3_8b_instruct.get_model()
        assert callable(model), "Loaded model is not callable."
        logging.info("Model loaded successfully.")
        return model
    except Exception as e:
        logging.error(f"Error loading model: {e}")
        raise


def test_inference(model, prompt: str):
    try:
        response = model(prompt)
        assert isinstance(response, str), "Response is not a string."
        assert len(response.strip()) > 0, "Empty response."
        logging.info(f"Inference successful: {response.strip()}")
        return response
    except Exception as e:
        logging.error(f"Inference failed: {e}")
        raise


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", type=str, default="What is the capital of France?", help="Prompt to test inference")
    args = parser.parse_args()

    check_env()
    model = load_model()
    test_inference(model, args.prompt)


if __name__ == "__main__":
    main()
