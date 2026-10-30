"""Demonstration: advance an existing order through the full status flow."""
import argparse
import json
import urllib.request


def main():
    # Read the order ID from the command line instead of hard-coding it.
    parser = argparse.ArgumentParser(description="Advance a MiniDash order")
    parser.add_argument("order_id", type=int)
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    args = parser.parse_args()
    for status in ["PREPARING", "READY", "PICKED_UP", "DELIVERED"]:
        # The REST endpoint remains the only source of state changes.
        body = json.dumps({"status":status}).encode("utf-8")
        request = urllib.request.Request(
            f"{args.base_url}/orders/{args.order_id}/status",
            data=body, headers={"Content-Type":"application/json"}, method="PATCH")
        with urllib.request.urlopen(request) as response:
            order = json.load(response)
            print(f"{status}: ETA={order['eta_at']}")


if __name__ == "__main__":
    main()
