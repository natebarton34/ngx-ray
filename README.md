# NgX-Ray
A Playwright-Powered Visibility & Permission Analyzer for AngularJS Applications
---

NgX-Ray is a security and front-end observability tool that scans AngularJS applications for:

🔍 Hidden DOM elements (ng-hide, ng-if, ng-show, display:none, etc.)

🔑 AngularJS scope permission variables

🌐 Permission-like data in JSON network responses

Then bundles them all into a:

🖥️ Tkinter interface with live search + tabbed results

---

This tool helps developers understand what UI elements are suppressed and how permission logic works in a web app without  access to the source code.

✨ Features
✔️ DOM Hidden Element Scanner

Identifies:

ng-hide, ng-if, ng-show

CSS-based invisibility

[hidden] attributes

Associated metadata (id, classList, data-qa-id, etc.)

✔️ AngularJS Scope Permission Collector

Recursively walks AngularJS scopes to find:

role variables

permission flags

"can*" variables

booleans, numbers, and strings

✔️ Network Response Permission Miner

Intercepts JSON responses and finds:

permissions

roles

canView, canEdit, allowed, enabled, etc.

✔️ Tkinter Desktop UI

3 Tab interface

Live search

Auto-grouped results

Browser launches automatically using Playwright
