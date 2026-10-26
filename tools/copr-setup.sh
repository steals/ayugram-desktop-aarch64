#!/usr/bin/env bash
# One-time COPR project setup. Usage: tools/copr-setup.sh <owner/project> <git clone url>
set -euo pipefail

project=${1:?owner/project}
clone_url=${2:?git clone url}
name=${project#*/}

copr-cli create "$name" \
  --chroot fedora-43-aarch64 \
  --chroot fedora-44-aarch64 \
  --chroot fedora-45-aarch64 \
  --enable-net on \
  --description "Unofficial AyuGram Desktop builds for Fedora (aarch64)" \
  --instructions "sudo dnf copr enable $project && sudo dnf install ayugram-desktop (requires RPM Fusion free)"

for pkg in tg_owt ayugram-desktop; do
  copr-cli add-package-scm "$name" \
    --name "$pkg" \
    --clone-url "$clone_url" \
    --commit main \
    --subdir "$pkg" \
    --spec "$pkg.spec" \
    --type git \
    --method make_srpm
done

echo "Build order: tg_owt first, then ayugram-desktop:"
echo "  copr-cli build-package $name --name tg_owt --timeout 108000"
echo "  copr-cli build-package $name --name ayugram-desktop --timeout 108000"
