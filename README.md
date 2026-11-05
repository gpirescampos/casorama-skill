# Casorama skill

Casorama helps a prospective buyer explore the potential of a property from listing photos. It guides style and renovation choices, generates illustrative room concepts using an available image-editing tool, and creates a standalone before/after report.

The skill focuses on keeping the original architecture recognisable and on visual consistency between different views of the same space. AI images are concepts, not measurements, structural assessments, renovation plans or cost estimates.

## Contents

- `skills/casorama/SKILL.md` — platform-neutral workflow.
- `skills/casorama/assets/report-template.html` — reusable report design.
- `skills/casorama/scripts/build_report.py` — standard-library Python report builder.
- `skills/casorama/agents/openai.yaml` — optional Codex interface metadata.

## Install and use

Use your agent platform's skill-installation method to install the `skills/casorama` directory, preserving its subdirectories. For a local Codex installation, copy that directory to `~/.codex/skills/casorama`; if a skill already exists there, review it before replacing it. Start a new session if the skill is not immediately available.

Invoke `$casorama` in a supporting agent, followed by a property listing URL or photos. The skill asks about the desired spaces, style, colours, renovation scope and furniture. It uses answers already supplied and proceeds one question at a time when clarification is needed.

An image editor capable of editing a supplied photo is required to generate concepts. A tool that can also accept a separate reference image improves cross-view consistency. Access to listing photos depends on the website and the platform's browser or connector capabilities. If those tools are unavailable, the skill explains the limitation and can prepare prompts instead. Availability, costs and permissions depend on the host; no particular model or provider is bundled.

The report builder requires Python 3 and uses only the standard library. It embeds images in the HTML, so the finished report opens offline. Its manifest format and command are described in the skill instructions. Platforms without Python or a persistent filesystem need their own supported file-creation workflow.

## Privacy and sharing

Property runs, downloaded photos, generated concepts, manifests and reports can contain personal information or copyrighted material. A standalone report embeds the photographs: sharing the HTML also shares its images. Keep generated property folders out of a public repository, and review usage rights and privacy before sharing.

The report template includes a link to `https://casorama.pt`. The site may not be available. The project and skill do not automatically publish reports.

## License

MIT; see [LICENSE](LICENSE).
