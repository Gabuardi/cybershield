from typing import List


def asset_by_org_adapter(data: list) -> List:
    result = []
    for row in data:
        for asset in row:
            org_created = False
            for item in result:
                if item["org"] == asset["owner_org"]:
                    org_created = True
                    item["assets"].append(asset)
                    item["asset_id_list"].append(asset["asset_id"])
            if org_created is False:
                result.append({
                    "org": asset["owner_org"],
                    "assets": [asset],
                    "asset_id_list": [asset["asset_id"]]
                })
    return result
