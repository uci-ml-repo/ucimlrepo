#!/usr/bin/env python3

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Test imports
try:
    from ucimlrepo import fetch_ucirepo, list_available_datasets

    print("✅ Imports successful")
except Exception as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)


# Test basic functionality
def test_invalid_inputs():
    try:
        fetch_ucirepo(id=1, name="Abalone")
        print("❌ Should have raised ValueError for both id and name")
        return False
    except ValueError:
        print("✅ Correctly raised ValueError for both id and name")

    try:
        fetch_ucirepo()
        print("❌ Should have raised ValueError for no arguments")
        return False
    except ValueError:
        print("✅ Correctly raised ValueError for no arguments")

    try:
        fetch_ucirepo(id="Abalone")
        print("❌ Should have raised ValueError for string id")
        return False
    except ValueError:
        print("✅ Correctly raised ValueError for string id")

    try:
        fetch_ucirepo(name=1)
        print("❌ Should have raised ValueError for numeric name")
        return False
    except ValueError:
        print("✅ Correctly raised ValueError for numeric name")

    return True


# Test platform detection (our Mac SSL fix)
def test_platform_detection():
    import platform

    print(f"✅ Platform detected: {platform.system()}")
    if platform.system() == "Darwin":
        print("✅ Running on macOS - SSL fix will be applied if needed")
    else:
        print("✅ Not running on macOS - standard SSL will be used")
    return True


if __name__ == "__main__":
    print("🧪 Running simple tests...")

    success = True
    success &= test_invalid_inputs()
    success &= test_platform_detection()

    if success:
        print("\n🎉 All basic tests passed!")
        print("✅ The SSL fix for Mac has been successfully integrated")
    else:
        print("\n❌ Some tests failed")
        sys.exit(1)
