JS_HIDDEN_SCAN = """
(() => {
  const results = [];
  const all = document.querySelectorAll('*');

  all.forEach(el => {
    const styles = window.getComputedStyle(el);
    const hiddenReasons = [];

    if (el.classList.contains('ng-hide')) hiddenReasons.push('ng-hide class');
    if (el.hasAttribute('ng-hide')) hiddenReasons.push('ng-hide attribute');

    const ngIf = el.getAttribute('ng-if');
    const ngShow = el.getAttribute('ng-show');
    if (ngIf) hiddenReasons.push('ng-if: ' + ngIf);
    if (ngShow) hiddenReasons.push('ng-show: ' + ngShow);

    if (el.hidden) hiddenReasons.push('[hidden] attribute');
    if (styles.display === 'none') hiddenReasons.push('display:none');
    if (styles.visibility === 'hidden') hiddenReasons.push('visibility:hidden');

    if (!hiddenReasons.length) return;

    results.push({
      tag: el.tagName.toLowerCase(),
      id: el.id || null,
      classList: Array.from(el.classList),
      dataQaId: el.getAttribute('data-qa-id'),
      ngShow: ngShow || null,
      ngIf: ngIf || null,
      hiddenReasons: hiddenReasons
    });
  });

  return results;
})();
"""

def scan_dom_hidden(page):
    try:
        return page.evaluate(JS_HIDDEN_SCAN)
    except Exception:
        return []
