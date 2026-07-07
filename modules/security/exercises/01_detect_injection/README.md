# Detect Prompt Injection

## Theory
Untrusted user text may contain **instruction overrides** (`ignore instructions`, `system:`).

## Assignment
If input contains `ignore instructions`, print `INJECTION_DETECTED`. Else `SAFE`.
