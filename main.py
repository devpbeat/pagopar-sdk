from __future__ import annotations

import json
import os

from pagopar_sdk import PagoparClient


def main() -> None:
    """Run a small smoke check against `forma-pago/1.1/traer`.

    Required env vars:
        - PAGOPAR_PUBLIC_KEY
        - PAGOPAR_PRIVATE_KEY
    """

    public_key = os.getenv("PAGOPAR_PUBLIC_KEY")
    private_key = os.getenv("PAGOPAR_PRIVATE_KEY")

    if not public_key or not private_key:
        print("Set PAGOPAR_PUBLIC_KEY and PAGOPAR_PRIVATE_KEY before running this script.")
        return

    with PagoparClient(public_key=public_key, private_key=private_key) as client:
        response = client.commerce.get_payment_methods()

    print(json.dumps(response, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
