from typing import List


def tickets_adapter(data: list) -> List:
    result = []
    for row in data:
        for ticket in row:
            result.append(ticket)
    return result


def attach_asset_info(tickets_by_org: dict):
    for org in tickets_by_org:
        for ticket in org["tickets"]:
            asset_info = None
            # asset info lookup
            for asset in org["assets"]:
                if asset["asset_id"] == ticket["asset"]:
                    asset_info = asset
                    break
            ticket["asset"] = asset_info
    return tickets_by_org
