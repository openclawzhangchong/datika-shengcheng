#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
端到端测试（Playwright Python）：加载 index.html，验证渲染、页数、关键文字与导出。
依赖： pip install playwright && playwright install chromium
用法： python test/test_e2e.py
退出码：0=通过，1=失败
"""
import os
import sys

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("缺少 playwright，请先执行：pip install playwright && playwright install chromium")
    sys.exit(1)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = "file:///" + os.path.join(ROOT, "index.html").replace("\\", "/")
SHOT_DIR = os.path.join(ROOT, "test", "screenshots")
os.makedirs(SHOT_DIR, exist_ok=True)

failures = []


def check(cond, msg):
    if cond:
        print("  [OK]   " + msg)
    else:
        print("  [FAIL] " + msg)
        failures.append(msg)


def main():
    print("== 端到端测试 ==")
    print("页面：" + HTML)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(HTML, wait_until="load")
        page.wait_for_timeout(800)

        # --- 默认渲染 ---
        print("-- 默认配置 --")
        check(page.locator(".page").count() == 2, "默认生成 2 页（客观+主观）")
        body = page.inner_text("body")
        check("答题卡" in body, "页面含『答题卡』标题")
        check("单项选择题" in body and "多项选择题" in body and "判断题" in body,
              "三类选择题分区存在")
        check("填空题" in body and "简答题" in body, "主观题填空/简答分区存在")
        check("2B" not in body and "铅笔" not in body, "卡面无 2B 铅笔提醒字样")
        check(len(errors) == 0, "无 JS 运行时错误：" + str(errors[:2]))

        # --- 批量模式 + 条形码 ---
        print("-- 批量模式 --")
        page.fill("#startNo", "20260001")
        page.fill("#endNo", "20260003")
        page.check("#batchChk")
        page.click("#btnGen")
        page.wait_for_timeout(1200)
        check(page.locator(".page").count() == 6, "3 个准考号 → 6 页")
        check(page.locator("svg").count() >= 6, "生成了条形码 SVG（正反面各 3）")
        # 第一张卡条码内容
        first_bar_no = page.locator(".barcode .barno").first.inner_text()
        check("20260001" in first_bar_no.replace(" ", ""), "首张卡条码号码为 20260001")
        page.screenshot(path=os.path.join(SHOT_DIR, "batch.png"), full_page=True)

        # --- 简答题分小题 ---
        print("-- 简答题分小题 --")
        page.uncheck("#batchChk")
        page.fill("#subq", "3")
        page.click("#btnGen")
        page.wait_for_timeout(600)
        check(page.locator(".sub-q").count() >= 9, "每题 3 小题 × 3 题 = 至少 9 个小题行")
        check("(1)" in page.inner_text("body") and "(3)" in page.inner_text("body"),
              "小题序号 (1)(2)(3) 已标注")
        page.screenshot(path=os.path.join(SHOT_DIR, "subq3.png"), full_page=True)

        browser.close()

    print()
    if failures:
        print("端到端测试未通过，共 %d 项失败。" % len(failures))
        return 1
    print("端到端测试全部通过。截图目录：" + SHOT_DIR)
    return 0


if __name__ == "__main__":
    sys.exit(main())
