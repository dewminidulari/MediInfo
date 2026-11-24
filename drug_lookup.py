import requests

URL = "https://api.fda.gov/drug/label.json"

def first(data, key, default="Not available"):
    value = data.get(key)
    return value[0] if value else default

def get_drug_info(name):
 
    for field in ("openfda.generic_name", "openfda.brand_name"):
        params = {"search": f'{field}:"{name}"', "limit": 1}
        r = requests.get(URL, params=params, timeout=30)
        if r.status_code != 200:
            continue
        data = r.json()["results"][0]
        openfda = data.get("openfda", {})
        return {
            "generic_name": first(openfda, "generic_name"),
            "brand_name": first(openfda, "brand_name"),
            "uses": first(data, "indications_and_usage"),
            "warnings": first(data, "warnings"),
            "side_effects": first(data, "adverse_reactions"),
            "interactions": first(data, "drug_interactions"),
            "source": "openFDA (U.S. FDA drug labels)",
        }
    return None

if __name__ == "__main__":
    info = get_drug_info("amoxicillin")
    print(info if info else "Not found")