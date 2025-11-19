# NgX-Ray  
A Playwright-Powered Visibility & Permission Analyzer for AngularJS Applications

---

NgX-Ray is a diagnostic and observability tool designed to reveal hidden UI logic inside AngularJS applications — even when the source code isn’t available.

It performs three deep inspections:

🛠️ **Hidden DOM element detection** (`ng-hide`, `ng-if`, `ng-show`, CSS visibility rules, etc.)  
🧩 **AngularJS scope permission extraction** (roles, permission flags, allow/can*, enabled states)  
📡 **Network JSON permission mining** (server-side authorization indicators)

Then bundles all results into a clean, interactive:

🖥️ **Tkinter desktop interface** with live search and organized tabs

This helps developers, testers, and security analysts understand how UI visibility, permissions, and authorization rules behave across dynamic AngularJS applications.

---

## ✨ Features

### ✔️ DOM Hidden Element Scanner  
Detects UI elements that are hidden due to:

- AngularJS directives (`ng-hide`, `ng-if`, `ng-show`)  
- CSS-based invisibility  
- Native `[hidden]` attributes  
- Additional metadata (`id`, `classList`, `data-qa-id`, etc.)

### ✔️ AngularJS Scope Permission Collector  
Recursively explores AngularJS scopes to uncover permission-related values such as:

- role variables  
- boolean permission flags  
- `"can*"` variables  
- allow/enabled fields  
- strings, numbers, and booleans stored in scope trees

### ✔️ Network Response Permission Miner  
Intercepts JSON responses to extract authorization-related fields:

- `permissions`  
- `roles`  
- `canView`, `canEdit`, `allowed`, `enabled`, etc.

### ✔️ Tkinter Desktop UI  
Provides an accessible interface with:

- 📁 Three structured tabs (DOM Hidden Elements, AngularJS Permissions, Network Permissions)  
- 🔎 Live search across all tabs  
- 🧮 Auto-formatted, grouped result sets  
- 🌐 Automatic Chromium browser launch powered by Playwright

---
# Installation
git clone https://github.com/natebarton34/ngx-ray
cd ngx-ray/src
pip install -r requirements.txt
playwright install
python main.py



