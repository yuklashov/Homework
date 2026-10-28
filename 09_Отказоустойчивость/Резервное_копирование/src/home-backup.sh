#!/usr/bin/env bash
# Linux: ежедневное полное зеркало. Удаляет лишнее только в целевой копии.
set -euo pipefail
umask 077
source_dir=${BACKUP_SOURCE_DIR:-"$HOME"}
target_dir=${BACKUP_TARGET_DIR:-/tmp/backup}
lock_held=0
lock_dir=''
finish() {
    rc=$?
    trap - EXIT
    if [ "$lock_held" -eq 1 ]; then rmdir "$lock_dir" || true; fi
    if [ "$rc" -eq 0 ]; then status=SUCCESS; else status=FAIL; fi
    if ! logger -t netology-home-backup -- "$status rc=$rc source=$source_dir target=$target_dir"; then
        printf '%s\n' "Не удалось записать результат $status в системный журнал" >&2
        if [ "$rc" -eq 0 ]; then rc=1; fi
    fi
    exit "$rc"
}
trap finish EXIT
[ -d "$source_dir" ]
[ ! -L "$target_dir" ]
mkdir -p "$target_dir"
source_dir=$(cd "$source_dir" && pwd -P)
target_dir=$(cd "$target_dir" && pwd -P)
[ "$source_dir" != / ] && [ "$target_dir" != / ]
case "$target_dir/" in "$source_dir/"*) echo 'Цель внутри источника' >&2; exit 2;; esac
case "$source_dir/" in "$target_dir/"*) echo 'Источник внутри цели' >&2; exit 2;; esac
lock_dir="${target_dir}.lock"
mkdir "$lock_dir"
lock_held=1
rsync -a --checksum --delete -- "$source_dir/" "$target_dir/"
