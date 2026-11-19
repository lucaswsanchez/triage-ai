# Knowledge base data

The files in `kb/` and `processes/` are copied verbatim from
[lucaswsanchez/helpdesk-kb](https://github.com/lucaswsanchez/helpdesk-kb) (MIT License,
commit `b109a04`). The rendered articles live at <https://lucaswsanchez.github.io/helpdesk-kb/>.

- `kb/kb-*.md`: 21 help desk articles with YAML front matter (`id`, `title`, `category`, `level`, `tags`).
- `processes/priority-matrix.md`: impact × urgency matrix used to compute ticket priority.

To refresh them, run `python -m scripts.sync_kb` from `backend/`.
