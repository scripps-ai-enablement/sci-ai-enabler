#!/usr/bin/env bash
# Regenerate the `dropdown` block in recipe-feedback.yml and tool-feedback.yml
# from the current set of recipes/items/*.md and catalog/tools/*.md.
# Idempotent: writes nothing if content is unchanged.
set -euo pipefail

regen_form() {
  local form="$1"
  local items_glob="$2"
  local block_id="$3"   # the `id:` of the dropdown to replace

  # Collect slugs, sorted, excluding index.md
  local slugs
  slugs=$(ls $items_glob 2>/dev/null | grep -v '/index.md$' | xargs -n1 basename | sed 's/\.md$//' | sort)

  # Build the new options block as YAML lines (prefixed with 8 spaces for indent under `options:`)
  local opts
  opts=$(printf '        - %s\n' $slugs)
  opts="${opts}"$'\n        - Not listed'

  # In-place rewrite: replace the lines from `    id: $block_id` down to the next field id (or end of body),
  # specifically only the `options:` list. Use python for reliable YAML-ish edit.
  python3 - "$form" "$block_id" <<'PY' "$opts"
import re, sys, pathlib
path = pathlib.Path(sys.argv[1])
block_id = sys.argv[2]
new_opts = sys.argv[3]
text = path.read_text()

# Pattern: find the dropdown with the right id, then replace its `options:` body.
# Does NOT use re.DOTALL so it cannot cross `  - type:` boundaries between fields.
# Matches: the `id: <block_id>` line, then any lines that don't start a new field
# (i.e., not starting with `  - type:`), then `      options:\n`, then the option lines.
pattern = re.compile(
    r"(    id:\s*" + re.escape(block_id) + r"(?:\n(?!  - type:)[^\n]*)*\n      options:\n)(?:        - [^\n]*\n)+",
)
new_text, n = pattern.subn(lambda m: m.group(1) + new_opts + "\n", text, count=1)
if n != 1:
    sys.stderr.write(f"ERROR: did not match exactly one options block for id={block_id} in {path}\n")
    sys.exit(1)
if new_text != text:
    path.write_text(new_text)
    print(f"updated {path}")
else:
    print(f"unchanged {path}")
PY
}

regen_form ".github/ISSUE_TEMPLATE/recipe-feedback.yml" "recipes/items/*.md" "recipe"
regen_form ".github/ISSUE_TEMPLATE/tool-feedback.yml"   "catalog/tools/*.md"  "tool"
