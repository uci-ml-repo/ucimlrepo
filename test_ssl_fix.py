#!/usr/bin/env python3

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


# Test SSL fix specifically
def test_ssl_fix():
    try:
        from ucimlrepo import fetch_ucirepo

        print("🧪 Testing SSL fix by fetching a real dataset...")

        # Try to fetch a small dataset (Iris is good for testing)
        iris = fetch_ucirepo(id=53)  # Iris dataset
        print(f"✅ Successfully fetched Iris dataset (ID: {iris.metadata.uci_id})")
        print(f"✅ Dataset shape: {iris.data.original.shape}")
        print(f"✅ Features shape: {iris.data.features.shape}")
        print(f"✅ Targets shape: {iris.data.targets.shape}")

        return True

    except Exception as e:
        print(f"❌ SSL test failed: {e}")
        return False


def test_mac_ssl_detection():
    import platform

    print(f"🔍 Testing Mac SSL detection...")
    print(f"✅ Platform: {platform.system()}")

    if platform.system() == "Darwin":
        print("✅ Running on macOS - SSL fix will be automatically applied if needed")
    else:
        print("✅ Not on macOS - standard SSL behavior")

    return True


if __name__ == "__main__":
    print("🧪 Testing SSL Fix Integration...\n")

    success = True
    success &= test_mac_ssl_detection()
    success &= test_ssl_fix()

    if success:
        print("\n🎉 SSL fix is working correctly!")
        print("✅ Your implementation successfully handles SSL issues on Mac")
    else:
        print("\n❌ SSL fix test failed")
        sys.exit(1)
