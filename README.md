# AyuGram Desktop — Fedora aarch64 (COPR)

Unofficial RPM packaging of [AyuGram Desktop](https://github.com/AyuGram/AyuGramDesktop)
for Fedora, built natively on aarch64 in [COPR](https://copr.fedorainfracloud.org/).
Primary target: Fedora Asahi Remix (Apple Silicon, 16K pages).

Not affiliated with Radolyn Labs.

## Install

```sh
# RPM Fusion free is required (ffmpeg)
sudo dnf install https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
sudo dnf copr enable OWNER/ayugram
sudo dnf install ayugram-desktop
```

## Layout

| Path | Purpose |
|---|---|
| `ayugram-desktop/` | Main package. Spec based on RPM Fusion (Ivan Romanov), `-full.tar.gz` upstream source |
| `tg_owt/` | WebRTC fork. RPM Fusion rawhide spec, `Release: 100.*` to win over RPM Fusion's build |
| `.copr/Makefile` | `make_srpm` entry point: `spectool -g` + `rpmbuild -bs` |
| `.github/workflows/bump.yml` | Daily: new upstream release → `rpmdev-bumpspec` → push → `copr-cli build-package` |
| `tools/copr-setup.sh` | One-time COPR project and package creation |

## Setup

1. Create a COPR API token at <https://copr.fedorainfracloud.org/api/>, save it to `~/.config/copr`.
2. `tools/copr-setup.sh OWNER/ayugram https://github.com/OWNER/ayugram-fedora.git`
3. Build `tg_owt` first, then `ayugram-desktop` (commands are printed by the script).
4. GitHub repo settings:
   - secret `COPR_CONFIG` — contents of `~/.config/copr`;
   - variable `COPR_PROJECT` — `OWNER/ayugram`.

## Maintenance

- **AyuGram bumps** are automatic. A failed COPR build usually means tg_owt or a Qt/protobuf patch needs updating.
- **tg_owt** is manual: take the commit AyuGram/tdesktop pins, update `commit0`/`date`
  (and bundled `commit1..4` if upstream changed submodules), bump the Release suffix, keep it `>= 100`.
- **Verify on Asahi** after the first build of each Fedora release:
  - `ldd /usr/bin/AyuGram | grep jemalloc` — must be Fedora's system jemalloc, not a bundled one;
  - start AyuGram and make a test call (tg_owt path).

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| `nothing provides cmake(tg_owt)` | tg_owt not built yet in this chroot, or the RPM Fusion repo is missing |
| `nothing provides pkgconfig(openh264)` | Cisco openh264 repo is disabled in the chroot — add it as an external repo |
| Build killed / timeout | Pass `--timeout 108000`; LTO must stay off on aarch64 |
| `cmake(tde2e)` / `cmake(ada)` missing | Fedora release too old for this AyuGram version — drop that chroot |
