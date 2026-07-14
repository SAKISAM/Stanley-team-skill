#!/usr/bin/env bash

set -euo pipefail

usage() {
  echo "Usage: $0 <@handle|x.com/profile-url> <overview|growth|risk|monetization>" >&2
}

if [ "$#" -ne 2 ]; then
  usage
  exit 2
fi

raw_handle="$1"
mode="$2"

if [[ "$raw_handle" =~ ^https?://(www\.)?(x\.com|twitter\.com)/([A-Za-z0-9_]{1,15})(/.*)?$ ]]; then
  handle="${BASH_REMATCH[3]}"
elif [[ "$raw_handle" =~ ^@?([A-Za-z0-9_]{1,15})$ ]]; then
  handle="${BASH_REMATCH[1]}"
else
  echo "Invalid X handle or profile URL: $raw_handle" >&2
  exit 2
fi

case "$mode" in
  overview)
    focus="主页表达、最近 30 天公开内容主题、更新节奏、互动情况和最明显的问题"
    ;;
  growth)
    focus="最近 30 天哪些公开内容可能带来关注，哪些内容曝光或互动弱，以及主页到关注的承接问题"
    ;;
  risk)
    focus="最近 30 天公开内容和互动中可能出现的重复、模板化、垃圾互动、敏感内容或异常行为线索"
    ;;
  monetization)
    focus="最近 30 天公开内容中可能影响创作者收益的内容与行为线索，包括平台操纵、重复内容、成人或敏感内容、版权和商业披露"
    ;;
  *)
    usage
    exit 2
    ;;
esac

grok_bin="$(command -v grok 2>/dev/null || true)"
if [ -z "$grok_bin" ] && [ -x "$HOME/.grok/bin/grok" ]; then
  grok_bin="$HOME/.grok/bin/grok"
fi
if [ -z "$grok_bin" ]; then
  echo "Grok CLI is not installed. See references/grok-cli-guide.md." >&2
  exit 3
fi

tmp_dir="$(mktemp -d 2>/dev/null || mktemp -d -t achuan-x-grok)"
stderr_file="$tmp_dir/grok-stderr.log"
result_file="$tmp_dir/grok-result.txt"
trap 'rm -rf "$tmp_dir"' EXIT

prompt="请使用 X 搜索，只查看 @${handle} 的公开主页和公开帖子，重点检查：${focus}。

要求：
1. 先确认检索到的账号确实是 @${handle}；无法确认就停止并说明。
2. 优先查看最近 30 天；数据不足时写清实际看到的时间范围。
3. 分成：看得到的事实、可能的问题、还缺什么证据、建议 Codex 下一步向用户问什么。
4. 关键判断附帖子链接和发布日期，最多保留 10 条证据。
5. 不要把猜测写成平台判定，不要断言账号被影子封禁或违反收益规则。
6. 不要尝试登录、发帖、删帖、申诉或修改账号。
7. 用简体中文，写给另一个 X 运营顾问看，简洁具体。
8. 不输出搜索过程或“正在检查”之类的进度，只输出完成后的最终报告。"

if ! "$grok_bin" \
  --cwd "$tmp_dir" \
  --verbatim \
  --no-plan \
  --no-memory \
  --no-subagents \
  --max-turns 10 \
  --output-format plain \
  -p "$prompt" >"$result_file" 2>"$stderr_file"; then
  echo "Grok account research failed." >&2
  if [ -s "$stderr_file" ]; then
    tail -n 20 "$stderr_file" >&2
  fi
  exit 4
fi

# Grok 偶尔会在正式报告前输出一句进度说明。有 Markdown 标题时，只返回报告本体。
if grep -q '^# ' "$result_file"; then
  sed -n '/^# /,$p' "$result_file"
else
  cat "$result_file"
fi
