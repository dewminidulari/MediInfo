from drug_lookup import get_drug_info
from explain import explain

name = "ibuprofen"

info = get_drug_info(name)

if info is None:
    print("Medicine not found.")
else:
    print(explain(info))
    print("\nSource:", info["source"])