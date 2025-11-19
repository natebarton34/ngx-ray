import json

def collect_permission_like(obj, prefix, out, depth=0, max_depth=6):
    if depth > max_depth:
        return

    if isinstance(obj, dict):
        for key, value in obj.items():
            path = f"{prefix}.{key}" if prefix else key
            k = key.lower()

            is_perm_field = (
                "perm" in k or
                k.startswith("can") or
                "allow" in k or
                "enabled" in k or
                k == "role" or
                k.endswith("role") or
                k == "permissions"
            )

            if is_perm_field and isinstance(value, (bool, str, int, float)):
                out.append({"path": path, "value": value, "type": type(value).__name__})

            if isinstance(value, (dict, list)):
                collect_permission_like(value, path, out, depth + 1, max_depth)

    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            collect_permission_like(v, f"{prefix}[{i}]", out, depth + 1, max_depth)


def attach_network_listener(page, store):
    def handle_response(resp):
        try:
            content_type = resp.headers.get("content-type", "")
            if "application/json" not in content_type:
                return
            text = resp.text()
            data = json.loads(text)
        except Exception:
            return

        hits = []
        collect_permission_like(data, "", hits)
        for h in hits:
            store.append({
                "url": resp.url,
                "path": h["path"],
                "value": h["value"],
                "type": h["type"]
            })

    page.on("response", handle_response)
