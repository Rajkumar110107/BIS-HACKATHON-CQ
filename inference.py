import json
import argparse
import time
from src.pipeline import Pipeline


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    pipe = Pipeline()

    with open(args.input, "r", encoding="utf-8") as f:
        queries = json.load(f)

    results = []

    for q in queries:
        start = time.time()

        query = q.get("query", "")
        q_id = q.get("id", None)

        codes = pipe.run(query)

        end = time.time()

        results.append({
            "id": q_id,
            "retrieved_standards": codes,
            "latency_seconds": round(end - start, 3)
        })

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("Inference complete!")


if __name__ == "__main__":
    main()