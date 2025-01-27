import json

with open(r"out\SoccerNetResults\final_results.json", "r") as file:
    model_output = json.load(file)

with open(r"data\SoccerNet\test\test_gt.json", "r") as file:
    ground_truth = json.load(file)


def is_implicit_int(key):
    try:
        int(key)
        return True
    except ValueError:
        return False


def find_differences(model_output, ground_truth):
    differences = []

    for key in model_output.keys() | ground_truth.keys():
        if not is_implicit_int(key):
            continue

        if key not in ground_truth:
            differences.append(
                {
                    "path": key,
                    "message": f"Key '{key}' is missing in Ground Truth JSON.",
                }
            )
            continue

        if key not in model_output:
            differences.append(
                {
                    "path": key,
                    "message": f"Key '{key}' is missing in Model Output JSON.",
                }
            )
            continue

        model_value = model_output[key]
        ground_value = ground_truth[key]

        if isinstance(model_value, (int, str)) and isinstance(ground_value, (int, str)):
            model_value = str(model_value)
            ground_value = str(ground_value)

        if model_value != ground_value:
            differences.append(
                {
                    "path": key,
                    "message": f"Value mismatch: {model_output[key]} (Model Output) vs {ground_truth[key]} (Ground Truth)",
                }
            )

    differences = sorted(differences, key=lambda x: int(x["path"]))
    return differences


differences = find_differences(model_output, ground_truth)
with open(r"out\SoccerNetResults\diff.json", "w") as diff_file:
    json.dump(differences, diff_file, indent=4)

if differences:
    print("Differences found")
else:
    print("The two JSON files are identical")
