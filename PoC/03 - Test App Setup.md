A local AngularJS-style demo app is used for safe testing.  

It includes:
- ng-hide, ng-if, ng-show  
- CSS-hidden elements  
- AngularJS permission flags  
- Fake JSON permissions API  
---
## 1. Create `index.html`
```html
<html ng-app="demoApp">
<head>
  <meta charset="utf-8" />
  <title>NgX-Ray Demo App</title>
  <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.8.2/angular.min.js"></script>
  <style>
    .admin-panel { border: 1px solid #ccc; margin: 20px; padding: 10px; }
    .hidden-banner { display: none; }
  </style>
</head>
<body ng-controller="MainCtrl as vm">

  <h1>NgX-Ray Demo</h1>

  <p>User role: <strong>{{ vm.userRole }}</strong></p>
  <p>canViewAdmin: <strong>{{ vm.canViewAdmin }}</strong></p>

  <!-- Hidden by Angular -->
  <div class="admin-panel"
       ng-show="vm.canViewAdmin">
    <h2>Admin Panel</h2>
    <p data-qa-id="admin-message">
      Only visible when <code>vm.canViewAdmin === true</code>
    </p>
  </div>

  <!-- Hidden by ng-if -->
  <div ng-if="vm.permissions.viewSecret"
       data-qa-id="secret-widget">
    <h3>Secret Widget</h3>
    <p>permissions.viewSecret is true.</p>
  </div>

  <!-- Hidden by CSS -->
  <p class="hidden-banner">
    This banner is hidden with display:none
  </p>

  <script>
    angular.module('demoApp', [])
      .controller('MainCtrl', function($http) {
        var vm = this;
        vm.userRole = 'standardUser';
        vm.canViewAdmin = false;
        vm.permissions = {
          viewSecret: false,
          canEditSettings: true
        };

        // Fake network call with permission-like JSON
        $http.get('/api/demo-permissions');
      });
  </script>
</body>
</html>
```
---
## 2. Create `server.py`
```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os

class DemoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'

        if self.path == '/api/demo-permissions':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            data = {
                "user": {
                    "role": "standardUser",
                    "permissions": {
                        "canViewAdmin": False,
                        "canEditSettings": True,
                        "viewSecret": False
                    }
                }
            }
            self.wfile.write(json.dumps(data).encode('utf-8'))
            return

        try:
            file_path = self.path.lstrip('/')
            if not os.path.isfile(file_path):
                self.send_error(404, "File not found")
                return
            with open(file_path, 'rb') as f:
                content = f.read()
            self.send_response(200)
            if file_path.endswith('.html'):
                self.send_header('Content-Type', 'text/html')
            else:
                self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, str(e))

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8000), DemoHandler)
    print("Serving demo app at http://localhost:8000")
    server.serve_forever()

```
---
## 3. Run the Test App
```bash
python server.py
```
---
### 1. Enter `http://localhost:8000`

### 2. Click "Scan"
### 3. Log in if needed (not required for local demo)
### 4. NgX-Ray runs:
- DOM hidden element evaluation  
- AngularJS scope exploration  
- Network JSON listener & parser  

---
## 🖼️ Scan Button Clicked  
![[testapp_2.png|500]]

---
## 🖼️ Playwright Browser Launch  
![[testapp_1 1.png]]
