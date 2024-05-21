#!/usr/bin/env python
"""
long_description [An example of a step using MLflow and Weights & Biases]: Performs basic cleaning on the data and save the results in Weights & Biases
"""
import argparse
import logging
import wandb
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()
    logger.info("Downloading input artifact")
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(artifact_local_path)


    # Drop Outliers
    logger.info("Remove outliers in the price feature")
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()

    df['last_review'] = pd.to_datetime(df['last_review'])

    # Save the results to a CSV file
    logger.info("Save the processed data to csv")
    df.to_csv(args.output_artifact, index=False)

    # Build artifact
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )

    logger.info(f"Log artifact: {args.output_artifact}")
    artifact.add_file(args.output_artifact)
    run.log_artifact(artifact)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This steps cleans the data")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="The input artifact",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="The name for the cleaned data",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="The type of the cleaned data",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="Description of the preprocessed data",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="Min price to be considered",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="Max price to be considered",
        required=True
    )


    args = parser.parse_args()

    go(args)
