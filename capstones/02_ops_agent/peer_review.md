# Peer Review — Capstone 02 Ops Agent

## Before review
- [ ] Each tool runs via `tool` subcommand
- [ ] `run --task` completes eval task `t01` and `t02`
- [ ] `write_report` asks for confirmation
- [ ] Report JSON validates against schema

## Reviewer checklist
- [ ] `calculator` rejects unsafe input (no `import`, no letters)
- [ ] Agent stops at max steps without infinite loop
- [ ] Scratchpad content visible in logs or debug mode
- [ ] LLM receives tool results between steps
- [ ] `AGENT_DONE:n` matches actual tool calls
- [ ] No shell execution or arbitrary file write outside `out/`

## Demo script
```bash
python python/main.py run --data ./data --task "Find discount cap and compute 15% of 12000"
python python/main.py eval
```

## Questions for the author
1. How does the agent recover from a wrong tool choice?
2. Why require human confirm only for write?
3. What would you add for production deployment?

## Approve
All boxes checked + `EVAL:3/3` on reviewer's machine.
