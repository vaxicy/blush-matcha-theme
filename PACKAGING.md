# Packaging

```bash
python scripts/package.py            # add --force to overwrite an existing ZIP
```

The script reads `version` from `manifest.json` and writes
`blush-matcha-theme-<version>.zip`, keeping `manifest.json` at the root of the
archive. A copy stays in `dist/` and the release copy lands in the folder above
`Chrome-themes/`, so it is ready to drag into the Chrome Web Store dashboard.

## What the ZIP contains

| Entry | Why |
|-------|-----|
| `manifest.json` | The theme itself |
| `logo/logo128.png` | Referenced by the manifest `icons` field |
| `README.md` | Repository documentation |

## What stays out

| Excluded | Why |
|----------|-----|
| `store-assets/screenshots/`, `store-assets/promo/` | Uploaded separately in the store listing form |
| `store-assets/ASSET-NOTES.md`, `store-assets/references/` | Working notes and intermediate render output |
| `store-assets/store-description.txt` | Pasted into the store listing form |
| `scripts/` | Asset generation and packaging tooling |
| `dist/`, `*.zip` | The packaging output itself |
| `.codebuddy/`, `.gitignore` | Local working memory and version control |
| `Cached Theme.pak` | Chrome's own packed-theme cache |

After a successful build the script re-reads the manifest from inside the
archive, confirms no tooling or store-listing files slipped in, and checks the
copy byte-for-byte against the local build.
