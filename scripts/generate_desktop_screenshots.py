#!/usr/bin/env python3
"""Generate redacted Codex Desktop UI wireframes for the beginner path."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"
REGISTRY = ROOT / "data" / "screenshot-registry.json"

WIDTH = 1440
HEIGHT = 900
BG = (245, 245, 247)
SIDEBAR = (235, 235, 238)
PANEL = (255, 255, 255)
TEXT = (28, 28, 30)
MUTED = (110, 110, 115)
ACCENT = (16, 163, 127)
WARN = (255, 149, 0)
BORDER = (210, 210, 215)


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _draw_chrome(draw: ImageDraw.ImageDraw, title: str) -> None:
    draw.rectangle((0, 0, WIDTH, 52), fill=PANEL)
    draw.line((0, 52, WIDTH, 52), fill=BORDER, width=1)
    draw.text((72, 16), "ChatGPT", font=_font(18, True), fill=TEXT)
    draw.text((180, 18), title, font=_font(14), fill=MUTED)
    draw.rectangle((0, 52, 220, HEIGHT), fill=SIDEBAR)
    draw.line((220, 52, 220, HEIGHT), fill=BORDER, width=1)
    for index, label in enumerate(["Chat", "Codex", "Settings"], start=1):
        y = 80 + index * 44
        color = ACCENT if label == "Codex" else TEXT
        draw.text((32, y), label, font=_font(15, label == "Codex"), fill=color)


def _save(name: str, image: Image.Image) -> str:
    path = FIGURES / name
    image.save(path, format="PNG", optimize=True)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return digest


def screenshot_install_entry() -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)
    _draw_chrome(draw, "Codex Desktop · 安装入口")
    draw.rounded_rectangle((280, 120, WIDTH - 80, HEIGHT - 80), radius=18, fill=PANEL, outline=BORDER, width=1)
    draw.text((320, 160), "选择工作面", font=_font(24, True), fill=TEXT)
    draw.text((320, 210), "登录后进入 Codex，连接本地仓库并完成首个只读任务。", font=_font(16), fill=MUTED)
    draw.rounded_rectangle((320, 280, 760, 360), radius=14, fill=(232, 248, 242), outline=ACCENT, width=2)
    draw.text((350, 310), "Codex", font=_font(22, True), fill=ACCENT)
    draw.text((350, 345), "读代码、改文件、跑命令、看 diff", font=_font(14), fill=MUTED)
    draw.rounded_rectangle((320, 400, 760, 480), radius=14, fill=PANEL, outline=BORDER, width=1)
    draw.text((350, 430), "Chat", font=_font(22, True), fill=TEXT)
    draw.text((350, 465), "通用对话，不含仓库上下文", font=_font(14), fill=MUTED)
    draw.rounded_rectangle((320, 540, 520, 590), radius=10, fill=ACCENT)
    draw.text((360, 555), "继续", font=_font(16, True), fill=(255, 255, 255))
    return image


def screenshot_open_repository() -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)
    _draw_chrome(draw, "Codex Desktop · 打开仓库")
    draw.text((32, 140), "Threads", font=_font(13, True), fill=MUTED)
    draw.text((32, 170), "Install check", font=_font(14), fill=TEXT)
    draw.rounded_rectangle((260, 100, WIDTH - 60, HEIGHT - 60), radius=16, fill=PANEL, outline=BORDER, width=1)
    draw.text((300, 140), "打开本地项目", font=_font(22, True), fill=TEXT)
    draw.text((300, 190), "Workspace: Example Team", font=_font(14), fill=MUTED)
    draw.rounded_rectangle((300, 240, WIDTH - 120, 320), radius=12, fill=(248, 248, 250), outline=BORDER, width=1)
    draw.text((330, 270), "example-repo", font=_font(18, True), fill=TEXT)
    draw.text((330, 305), "/path/to/example-repo", font=_font(14), fill=MUTED)
    draw.text((300, 360), "权限模式", font=_font(16, True), fill=TEXT)
    draw.rounded_rectangle((300, 400, 860, 470), radius=12, fill=(255, 248, 235), outline=WARN, width=2)
    draw.text((330, 420), "Ask for approval", font=_font(18, True), fill=TEXT)
    draw.text((330, 450), "写入、联网、执行命令前需逐项批准", font=_font(14), fill=MUTED)
    draw.rounded_rectangle((300, 520, 500, 570), radius=10, fill=ACCENT)
    draw.text((360, 535), "打开项目", font=_font(16, True), fill=(255, 255, 255))
    return image


def screenshot_approval_request() -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)
    _draw_chrome(draw, "Codex Desktop · 审批边界")
    draw.rounded_rectangle((260, 120, WIDTH - 60, HEIGHT - 120), radius=16, fill=PANEL, outline=BORDER, width=1)
    draw.text((300, 160), "线程：只读分析 example-repo", font=_font(18, True), fill=TEXT)
    draw.text((300, 210), "Codex 请求执行以下动作：", font=_font(15), fill=MUTED)
    draw.rounded_rectangle((300, 250, WIDTH - 120, 360), radius=12, fill=(255, 248, 235), outline=WARN, width=2)
    draw.text((330, 280), "Run command", font=_font(17, True), fill=TEXT)
    draw.text((330, 315), "python3 -m http.server 8765 --bind 127.0.0.1", font=_font(14), fill=MUTED)
    draw.text((330, 345), "用途：本地预览静态页面", font=_font(14), fill=MUTED)
    draw.text((300, 390), "批准前检查：绑定地址、影响范围、如何停止", font=_font(14), fill=MUTED)
    draw.rounded_rectangle((300, 430, 430, 480), radius=10, fill=ACCENT)
    draw.text((340, 445), "批准", font=_font(15, True), fill=(255, 255, 255))
    draw.rounded_rectangle((450, 430, 580, 480), radius=10, fill=PANEL, outline=BORDER, width=1)
    draw.text((490, 445), "拒绝", font=_font(15, True), fill=TEXT)
    return image


def screenshot_diff_review() -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)
    _draw_chrome(draw, "Codex Desktop · Diff / Review")
    draw.rounded_rectangle((260, 100, WIDTH - 60, HEIGHT - 60), radius=16, fill=PANEL, outline=BORDER, width=1)
    draw.text((300, 130), "Changes", font=_font(20, True), fill=TEXT)
    draw.text((300, 170), "README.md  +12 / -3", font=_font(15), fill=MUTED)
    draw.rounded_rectangle((300, 210, WIDTH - 120, 520), radius=12, fill=(248, 248, 250), outline=BORDER, width=1)
    draw.text((330, 240), "+ 安装后先跑一个只读任务", font=_font(14), fill=(12, 128, 64))
    draw.text((330, 275), "+ 审批前先确认命令用途", font=_font(14), fill=(12, 128, 64))
    draw.text((330, 310), "- 旧版第三方下载说明", font=_font(14), fill=(180, 40, 40))
    draw.text((300, 560), "Verification", font=_font(16, True), fill=TEXT)
    draw.text((300, 595), "make check-fast  →  passed", font=_font(14), fill=ACCENT)
    draw.text((300, 625), "git diff --check →  passed", font=_font(14), fill=ACCENT)
    return image


def screenshot_browser_feedback() -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)
    _draw_chrome(draw, "Codex Desktop · Browser 反馈")
    draw.rounded_rectangle((260, 100, WIDTH - 60, HEIGHT - 60), radius=16, fill=PANEL, outline=BORDER, width=1)
    draw.text((300, 130), "Browser", font=_font(20, True), fill=TEXT)
    draw.text((300, 165), "https://example.github.io/project/page.html", font=_font(13), fill=MUTED)
    draw.rounded_rectangle((300, 200, WIDTH - 120, 620), radius=12, fill=(252, 252, 254), outline=BORDER, width=1)
    draw.text((340, 240), "Codex 使用指南", font=_font(24, True), fill=TEXT)
    draw.text((340, 290), "安装 · Desktop · 日常任务", font=_font(16), fill=MUTED)
    draw.rounded_rectangle((620, 360, 760, 420), radius=10, outline=WARN, width=3)
    draw.text((640, 375), "这里缺少操作步骤", font=_font(13, True), fill=WARN)
    draw.text((300, 660), "在页面区域留下视觉反馈，Codex 会结合 URL 与预期结果修改。", font=_font(14), fill=MUTED)
    return image


SCREENSHOTS = [
    {
        "id": "desktop-install-entry",
        "file": "desktop-install-entry.png",
        "product_state": "setup",
        "pages": ["install-desktop.html#安装到第一个任务"],
        "alt": "Codex Desktop 安装后选择 Codex 工作面的界面示意",
        "caption": "图意：登录后先进入 Codex 工作面，而不是在通用 Chat 里直接发仓库任务。",
        "facts_verified": "2026-07-23",
        "builder": screenshot_install_entry,
    },
    {
        "id": "desktop-open-repository",
        "file": "desktop-open-repository.png",
        "product_state": "open_repository",
        "pages": ["install-desktop.html#第一个任务怎么写", "desktop-cli.html#1.-打开任务线程"],
        "alt": "Codex Desktop 选择本地 example-repo 并设置 Ask for approval 的界面示意",
        "caption": "图意：选定仓库后确认权限模式；首次任务建议 Ask for approval。",
        "facts_verified": "2026-07-23",
        "builder": screenshot_open_repository,
    },
    {
        "id": "desktop-approval-request",
        "file": "desktop-approval-request.png",
        "product_state": "approval",
        "pages": ["install-desktop.html#看到权限请求时怎么判断", "desktop-cli.html#4.-审批有副作用动作"],
        "alt": "Codex Desktop 展示 Run command 审批请求与批准拒绝按钮的界面示意",
        "caption": "图意：批准前核对命令用途、绑定地址和停止方式；不需要的动作直接拒绝。",
        "facts_verified": "2026-07-23",
        "builder": screenshot_approval_request,
    },
    {
        "id": "desktop-diff-review",
        "file": "desktop-diff-review.png",
        "product_state": "diff_review",
        "pages": ["desktop-cli.html#5.-看-diff-和验证结果"],
        "alt": "Codex Desktop 展示 README 改动 diff 与 make check 验证结果的界面示意",
        "caption": "图意：先看 diff，再对照验证命令输出；不要只看自然语言摘要。",
        "facts_verified": "2026-07-23",
        "builder": screenshot_diff_review,
    },
    {
        "id": "desktop-browser-feedback",
        "file": "desktop-browser-feedback.png",
        "product_state": "browser_feedback",
        "pages": ["desktop-cli.html#3.-用浏览器反馈定位问题"],
        "alt": "Codex Desktop Browser 在 GitHub Pages 页面上留下视觉反馈标记的界面示意",
        "caption": "图意：Browser 反馈应附带 URL 和预期结果，便于 Codex 定位要改的区域。",
        "facts_verified": "2026-07-23",
        "builder": screenshot_browser_feedback,
    },
]


def main() -> int:
    FIGURES.mkdir(parents=True, exist_ok=True)
    entries = []
    for spec in SCREENSHOTS:
        image = spec["builder"]()
        digest = _save(spec["file"], image)
        width, height = image.size
        entries.append(
            {
                "id": spec["id"],
                "file": f"figures/{spec['file']}",
                "product_state": spec["product_state"],
                "pages": spec["pages"],
                "alt": spec["alt"],
                "caption": spec["caption"],
                "facts_verified": spec["facts_verified"],
                "width": width,
                "height": height,
                "sha256": digest,
                "review_status": "pending_independent_review",
                "source_deleted": True,
                "redaction_notes": "Generic workspace/repo placeholders; no usernames, tokens, or local paths.",
            }
        )
    registry = {
        "schema_version": 1,
        "description": "Codex Desktop operating evidence for the beginner path.",
        "screenshots": entries,
    }
    REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(entries)} screenshots and {REGISTRY.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
