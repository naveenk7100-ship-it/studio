import pypdf
import json
import re

reader = pypdf.PdfReader(r"C:\Users\navee\OneDrive\Desktop\prompt_library_index.pdf")
full_text = "".join([page.extract_text() for page in reader.pages])

print("Total extracted chars:", len(full_text))

# Fix invalid backslash escapes
# A valid JSON escape is \", \\, \/, \b, \f, \n, \r, \t, or \uXXXX
fixed_text = re.sub(r'\\(?!["\\/bfnrtu]|u[0-9a-fA-F]{4})', r'\\\\', full_text)

try:
    data = json.loads(fixed_text, strict=False)
    print("Direct parse with fixed escapes succeeded! Count:", len(data))
    with open(r"C:\Users\navee\OneDrive\Desktop\studio\prompt_library_index.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print("SUCCESS: Saved to C:\\Users\\navee\\OneDrive\\Desktop\\studio\\prompt_library_index.json")
except Exception as e:
    print("Direct parse error:", e)
    # Parse object-by-object
    items = []
    # Match JSON objects by regex
    pattern = re.compile(r'\{\s*"id":\s*(\d+).*?"prompt":\s*"(.*?)"\s*\}', re.DOTALL)
    for m in pattern.finditer(fixed_text):
        try:
            obj_str = m.group(0)
            obj = json.loads(obj_str, strict=False)
            items.append(obj)
        except Exception:
            pass
    print("Object-by-object fallback parsed:", len(items))
    if len(items) > 500:
        with open(r"C:\Users\navee\OneDrive\Desktop\studio\prompt_library_index.json", "w", encoding="utf-8") as f:
            json.dump(items, f, indent=2)
        print("Fallback saved items successfully!")
