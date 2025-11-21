
This project grew out of an unexpected connection between an analytics platform I use daily for my sport and application security. While experimenting with this platform, I noticed something interesting: certain UI elements were clearly present in the DOM, but only surfaced under specific conditions. This inconsistency sparked my curiosity and became the seed for NgX-Ray.

---
## Takeaways from the Initial Experiment

### **1. Hidden UI Doesn’t Always Mean Missing UI**
On my teams analytics platform, some widgets, buttons, and panels appeared “missing” at first glance, but the underlying HTML was still present. This revealed an important pattern:

- Modern applications often hide elements dynamically  
- Visibility is controlled by more than simple CSS  
- Different user roles load the same frontend but see different UI

This directly inspired the DOM Hidden Element Scanner in NgX-Ray.

---
### **2. Permissions Often Exist in Multiple Layers**
I observed that some actions in the platform were enabled/disabled in ways that didn’t line up perfectly with visible UI.

This made me realize:
- Frontend visibility ≠ backend authorization  
- Permissions can live in:
  - JSON responses
  - AngularJS or client-side variables
  - Session or storage objects

This introduced the idea that **permission logic must be inspected from multiple angles**, not just the UI.

---
### **3.  Platform Logic**
The platforms' workflows taught me to:
- Identify patterns
- Look for hidden tendencies
- Understand why certain actions are allowed or blocked

NgX-Ray is a way to automate this probing of AngularJS applications.

---
## Takeaways from the Coding Experience

### **1. Modular Design Makes Everything Scalable**
Breaking the scanners into separate modules taught me:
- Single responsibility files make debugging far easier  
- Future improvements can be added without refactoring  
- UI and scanning logic should never live in the same file

This is the first time I built something at this scale with proper modular architecture.

---
### **2. Playwright Is One of the Most Powerful Tools for Real-World Analysis**
Through this project, I learned:
- `networkidle` detection matters for dynamic apps  
- Network interception opens the door to deep insights  
- The browser automation layer is more capable than most people think

Playwright is something I will without a doubt leverage in the future.

---
### **3. AngularJS Scope Exploration Is Way More Complex Than Expected**
AngularJS hides a lot of state behind:
- isolate scopes
- inherited scopes
- watch expressions

The recursive scanning logic was the most challenging part of the project, but it gave me:
- a deep understanding of AngularJS internals  
- improved debugging skills  
- more confidence in writing recursive, tree-based algorithms  

---
### **4. Building a UI Makes Your Tool Real**
Tkinter doesn't have the flashiest interface, but:
- Live search  
- Notebook tabs  
- Auto-refresh logic  
…turned this into a functional, usable tool, not just another script.

It forced me to think about:
- User experience  
- Data organization  
- How results should be presented, not just retrieved  

---
### **5. The Project Introduced Me to End-to-End Engineering**
From idea → PoC → architecture → UI → testing → documentation, this was a full lifecycle project.

How my skillset grew:
- Better Python structuring  
- Understanding real-world permission patterns  
- Strengthened debugging, recursion, and automation skills  
- Improved documentation (utilized Obsidian for PoC note keeping)

This is one of the first projects where I had to combine **soft skills, security thinking, and coding** into one deliverable.

