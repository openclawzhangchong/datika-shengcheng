# 项目交接文档（Handoff）

## 一句话简介

`datika-shengcheng` 是一个纯前端单文件答题卡生成器：按题量生成两页 A4 答题卡（客观题 / 主观题分面），支持批量预印条形码准考号，一键导出多页 PDF。

- 在线演示 / 官网：<https://openclawzhangchong.github.io/datika-shengcheng/>
- 仓库：<https://github.com/openclawzhangchong/datika-shengcheng>

## 当前状态（2026-11-19）

- 版本：v1.5.0
- 核心文件：`index.html`（单文件，全内嵌，双击可用）
- 部署：GitHub Pages，main 分支根目录，已上线
- 测试：结构校验 + Playwright 端到端（见 `test/`）

## 文件地图

| 路径 | 作用 |
| --- | --- |
| `index.html` | 程序本体 + Pages 首页 |
| `README.md` | 功能、用法、目录、测试 |
| `CHANGELOG.md` | 版本记录 |
| `docs/answer-sheet-spec.md` | 高考/中考答题卡版式调研 |
| `docs/lessons-learned.md` | 开发与踩坑经验 |
| `test/check_syntax.py` | 零依赖结构校验 |
| `test/test_e2e.py` | Playwright 端到端测试 |
| `test/smoke_test.mjs` | Node 冒烟测试 |
| `test/README.md` | 测试说明 |

## 核心实现要点（维护须知）

1. **单文件**：不要拆分成多文件，`index.html` 即全部。
2. **依赖**：html2canvas、jsPDF 走 CDN；JsBarcode 已内嵌，勿删。
3. **两页结构**：第 1 页客观题（选择填涂区），第 2 页主观题（填空 + 简答）。题号全局连续（单选→多选→判断→填空→简答）。
4. **条形码**：批量模式在条形码区生成 CODE128（`barcodeSvgHtml`），内容为准考号补足位数；正反两面同步。
5. **填空题**：每行 5 道并列（`.fill-grid`），分小题由 `subq` 控制，0 时保持整题大框。
6. **自适应**：`setRowHeight` 控制客观题行高；`subjectiveHtml` 内控制主观题高度。改动后务必端到端截图检查溢出。
7. **卡面文案**：不重复印刷"2B 铅笔"类提醒。

## 常见维护操作

- 改版式 → 编辑 `index.html` 的 `<style>` 与 `buildCard` / `page1Html` / `page2Html` / `subjectiveHtml`。
- 加功能 → 同时更新 `README.md` 功能表与 `CHANGELOG.md`。
- 发版 → 改 `CHANGELOG.md` 版本号，`git commit` 后 `git push`，Pages 自动更新（约 1-2 分钟）。
- 回归 → `python test/check_syntax.py` + `python test/test_e2e.py`。

## 已知边界 / 非目标

- 非任何考试院官方答题卡，仅通用化参考实现，不用于真实国家级考试。
- 只生成空白 / 预印号码的卡，不含题库、答案与判卷功能。
- 上限：客观题 120 题、批量 200 份（保证单页清晰与生成性能）。
