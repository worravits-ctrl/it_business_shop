import requests

try:
    print("Testing server...")
    
    # Test available routes
    routes_to_test = [
        '/',
        '/test', 
        '/login',
        '/simple-login'
    ]
    
    for route in routes_to_test:
        try:
            response = requests.get(f'http://127.0.0.1:8000{route}')
            print(f"{route}: Status {response.status_code}")
            if response.status_code == 302:
                print(f"  -> Redirects to: {response.headers.get('Location')}")
            elif response.status_code == 200:
                print(f"  -> Content: {response.text[:100]}...")
        except Exception as e:
            print(f"{route}: Error - {e}")
    
    print("=" * 50)
    
except Exception as e:
    print(f"Error: {e}")
    print("Make sure the server is running on port 8000")