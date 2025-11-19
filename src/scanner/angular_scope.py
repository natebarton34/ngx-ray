JS_ANGULAR_PERMISSIONS = """
(() => {
  if (!window.angular || !angular.element) return [];

  const results = [];
  const candidates = document.querySelectorAll('[ng-show], [ng-if]');

  function isObject(val) {
    return val && typeof val === 'object';
  }

  function collect(obj, prefix, out, visited) {
    if (!isObject(obj) || visited.has(obj)) return;
    visited.add(obj);

    for (const key in obj) {
      if (!obj.hasOwnProperty(key) || key.startsWith('$')) continue;

      let val;
      try { val = obj[key]; } catch { continue; }

      const path = prefix ? `${prefix}.${key}` : key;
      const lower = key.toLowerCase();

      const interesting =
        lower.includes('perm') ||
        lower.startsWith('can') ||
        lower.includes('allow') ||
        lower.includes('enabled') ||
        lower === 'role' ||
        lower.endsWith('role') ||
        lower === 'permissions';

      if (interesting && ['boolean','string','number'].includes(typeof val)) {
        out.push({ path, value: val, type: typeof val });
      }

      if (isObject(val)) collect(val, path, out, visited);
    }
  }

  candidates.forEach(el => {
    let scope;
    try {
      const ngElement = angular.element(el);
      scope = ngElement.isolateScope?.() || ngElement.scope?.();
    } catch { return; }

    if (!scope) return;

    const resultsList = [];
    collect(scope, '', resultsList, new Set());

    if (resultsList.length) {
      results.push({
        tag: el.tagName.toLowerCase(),
        dataQaId: el.getAttribute('data-qa-id'),
        ngShow: el.getAttribute('ng-show'),
        ngIf: el.getAttribute('ng-if'),
        permissions: resultsList
      });
    }
  });

  return results;
})();
"""

def scan_angular_permissions(page):
    try:
        return page.evaluate(JS_ANGULAR_PERMISSIONS)
    except Exception:
        return []
