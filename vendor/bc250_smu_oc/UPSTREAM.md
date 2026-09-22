# bc250_smu_oc, vendored

The SMU mailbox module of [bc250-collective/bc250_smu_oc](https://github.com/bc250-collective/bc250_smu_oc),
commit 43d6b4c (2026-01-26), MIT (see LICENSE), unchanged.

It ships in the skillfish-smu-oc package as /opt/bc250_smu_oc/bc250_smu, next
to bc250_apply.py, bc250_limits.py and stress_helper.py (identical to upstream)
and our bc250_detect.py, which live in system/opt/bc250_smu_oc/.

Why it is vendored (issue #96): the ISO installed it with pipx from GitHub into
/opt/pipx, best effort, while the Control Center, bc250-smu-oc.service and the
thermal guard all use /opt/bc250_smu_oc. Nothing installed it there, so on a
normal installation Tuner > CPU > Apply could not work.
