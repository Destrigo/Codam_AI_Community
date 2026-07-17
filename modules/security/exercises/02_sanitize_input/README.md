# Sanitize User Input

## Theory

Detecting an injection attempt (exercise 01) tells you *that* something is wrong; sanitizing
goes a step further and tries to neutralize it before the text ever reaches the model. The
[OWASP Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
lists input sanitization as one deterministic layer of defense — alongside structured
prompts (exercise 04) — with the caveat that stripping known bad phrases is a blocklist
approach: it catches what you thought of, not everything an attacker might try.

## Assignment

Given `"hello system: ignore instructions world"`, remove the substrings `ignore instructions`
and `system:`, keeping the rest of the text. Print `SANITIZED_OK:` followed by the cleaned
string.

## Verify

```bash
codam-labs --mock verify security/02_sanitize_input
```

Expected: output starting with `SANITIZED_OK:hello`

## Troubleshooting

- **Extra spaces left in the middle of the output** — `.replace("ignore instructions", "")`
  deletes the phrase but leaves the surrounding whitespace behind (`"hello system:  world"`
  → `"hello   world"`). `.strip()` only trims the *ends* of the string, not internal gaps —
  that's expected here and the check only requires the output to *start with* `SANITIZED_OK:hello`,
  but don't be surprised by the double spaces if you print the raw string to debug.
- **Removing the substrings in the wrong order changes nothing here, but can matter** — this
  specific input has no overlap between `ignore instructions` and `system:`, so order is safe
  today. If you generalize this function later, removing a shorter pattern first can
  accidentally destroy part of a longer one you still needed to match.
- **Sanitizing is not the same as detecting** — don't reuse exercise 01's boolean check here
  and print the *original* string when it "passes"; the assignment asks you to actually
  produce a *modified* string with the bad phrases gone, printed unconditionally.
