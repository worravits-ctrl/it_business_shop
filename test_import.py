try:
    import app_main
    print("Import successful")
except Exception as e:
    print(f"Import error: {e}")
    import traceback
    traceback.print_exc()
