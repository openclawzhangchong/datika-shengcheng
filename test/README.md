# 测试说明

本目录包含三类测试，从轻到重：

## 1. 结构校验（零依赖，最快）

```bash
python test/check_syntax.py
```

检查 `index.html` 的 HTML 结构、关键控件 id、关键实现标记、脚本括号配对、库是否内嵌。**不需要安装任何东西**。

## 2. 端到端测试（推荐）

先安装依赖（首次）：

```bash
pip install playwright
playwright install chromium
```

运行：

```bash
python test/test_e2e.py
```

覆盖：
- 默认 2 页结构、三类选择题、填空/简答分区
- 卡面无 "2B 铅笔" 字样
- 批量模式（3 个号 → 6 页）、条形码 SVG 与号码正确
- 简答题分小题：(1)(2)(3) 序号与小题行
- 无 JS 运行时错误

截图输出到 `test/screenshots/`。

## 3. 冒烟测试（Node）

用 `npx playwright screenshot` 截图，确认页面能渲染，无 Node 模块依赖：

```bash
npx playwright install chromium   # 首次
node test/smoke_test.mjs
```

## 说明

- 测试直接读取仓库根目录的 `index.html`（file:// 协议），无需启动服务器。
- GitHub 上不存放测试截图（`screenshots/` 已在 .gitignore）。
- 关键回归点见 [`../docs/lessons-learned.md`](../docs/lessons-learned.md)。
