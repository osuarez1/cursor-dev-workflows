# Commit messages: good vs weak

See [commits-logical-order.md](../docs/workflows/commits-logical-order.md).

## Weak

```text
Fixed the bug.
```

**Why weak:** No type; not imperative Conventional Commits subject.

---

```text
feat: updates
```

**Why weak:** Vague description; reviewer cannot tell what changed.

---

```text
feat(sales): Added manual reports.
```

**Why weak:** Past tense; trailing period on subject.

---

## Strong

```text
feat(sales): add manual report cost entry form

Validate overlapping date ranges server-side before save.

Closes PROJ-789
```

**Why strong:** Correct type and scope; imperative subject; body explains why; ticket footer.

---

```text
chore(deps): bump test runner to 3.2.1
```

**Why strong:** Narrow `chore` type; scope names the area; single logical change.
