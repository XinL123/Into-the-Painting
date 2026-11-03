# Qingming content audit
Goal: Check every published Qingming story/title against exact project images and primary evidence; correct unsupported assertions locally only.

1. Inventory and inspect all 13 crops and image provenance — complete.
2. Verify historical claims against museum records and period texts — complete, access limits documented.
3. Record per-claim verdicts and make conservative text corrections — complete.
4. Verify coordinates, build and local rendering — complete.

Outcome: AUDIT.md records title/claim-level verdicts for 13 stories and metadata; original-stories.json retains the 13 original titles/33 paragraphs. New copy has 27 paragraphs. Assets, hotspot geometry, sound and earlier timing work preserved. Local only; no commit/deployment.

Errors/limits: museum/article full pages timeout or TLS handshake/certificate errors; PDF size limit; NPM PDF 403. Accessible primary texts and index-only passages distinguished. Browser DOM shim lacks getAnimations; final screenshots and settled geometry used instead.
