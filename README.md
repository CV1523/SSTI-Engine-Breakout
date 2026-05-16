# SSTI-Engine-Breakout

A universal, cross-language Server-Side Template Injection (SSTI) research laboratory and breakout matrix. This repository tracks configuration files, operational lab scripts, and verification payloads used to map context disclosures, blind logical gates, and out-of-band (OAST) data exfiltration channels across diverse template engine runtimes.

---

### 🎛️ Active Multi-Engine Matrix

The project organizes independent laboratory servers into language-specific environments to isolate testing configurations.

#### 🐍 Python Environment (`/python`)
* Cheetah3
* Chameleon
* Django
* Jinja2 / Jinja2(sandbox)
* Mako
* Pystache (Mustache)
* SimpleTemplate
* Tornado

*Stay tuned for more breakouts as additional language environments are integrated!*

---

### 🤝 Contributing & Engine Expansion

Contributions are highly encouraged! If you want to expand this matrix with additional languages, patch security sandbox escapes, or document unique bypass chains, feel free to get involved.

#### How to Add a New Engine Lab:
1. Fork this repository and clone it to your local workspace.
2. Build out a standalone server script (e.g., Node.js/EJS, Java/Thymeleaf, PHP/Twig) that reflects input directly into a dynamic template compilation sequence.
3. Keep frontend layouts isolated in a dedicated HTML file.
4. Update the engine matrices inside this `README.md` and append any verified payload observations to the tracking docs.
5. Open a Pull Request detailing the engine version and breakout methodology.

---

### 📜 Acknowledgments & References

* Huge shoutout to the exceptional [Hackmanit Template Injection Table](https://cheatsheet.hackmanit.de/template-injection-table/) for providing the foundational structural breakdown, engine detection polyglots, and cross-framework comparison data that inspired these lab setups.