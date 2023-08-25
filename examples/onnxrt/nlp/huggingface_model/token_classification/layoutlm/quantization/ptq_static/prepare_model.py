import argparse
import os
import subprocess


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_model", type=str, required=False, default="microsoft/layoutlm-base-uncased")
    parser.add_argument("--output_model", type=str, required=True)
    return parser.parse_args()


def prepare_model(input_model, output_model):
    print("\nfine-tune model...")
    subprocess.run(
        [
            "python",
            "main.py",
            "--model_name_or_path",
            f"{input_model}",
            "--output_dir",
            "./layoutlm-base-uncased-finetuned-funsd",
            "--do_train",
            "--max_steps",
            "1000",
            "--warmup_ratio",
            "0.1",
        ],
        stdout=subprocess.PIPE,
        text=True,
    )

    subprocess.run(
        ["pip", "install", "optimum"],
        stdout=subprocess.PIPE,
        text=True,
    )

    print("\nexport model...")
    subprocess.run(
        [
            "optimum-cli",
            "export",
            "onnx",
            "--model",
            "./layoutlm-base-uncased-finetuned-funsd",
            f"{output_model}",
            "--task=token-classification",
        ],
        stdout=subprocess.PIPE,
        text=True,
    )

    assert os.path.exists(output_model), f"{output_model} doesn't exist!"


if __name__ == "__main__":
    args = parse_arguments()
    prepare_model(args.input_model, args.output_model)
