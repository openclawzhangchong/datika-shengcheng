#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
零依赖结构校验：检查 index.html 的关键结构与脚本完整性。
用法： python test/check_syntax.py
退出码：0=通过，1=失败
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(ROOT, "index.html")

REQUIRED_IDS = [
    "subject", "examName", "single", "multi", "judge", "blank", "short",
    "subq", "batchChk", "digits", "startNo", "endNo",
    "btnGen", "btnPdf", "btnPrint", "zoomIn", "zoomOut", "zoomLabel",
    "sheetWrap",
]

REQUIRED_TOKENS = [
    "html2canvas", "jspdf", "JsBarcode", "CODE128",
    'class="page"', "barcodeSvgHtml", "setRowHeight", "subjectiveHtml",
]

failures = []


def check(cond, msg):
    if cond:
        print("  [OK]   " + msg)
    else:
        print("  [FAIL] " + msg)
        failures.append(msg)


def main():
    print("== 结构校验：index.html ==")
    if not os.path.exists(HTML):
        print("找不到 index.html：" + HTML)
        return 1
    with open(HTML, encoding="utf-8") as f:
        html = f.read()
    print("文件大小：%d 字节" % len(html))

    check(html.lstrip().lower().startswith("<!doctype html>"), "HTML 文档声明")
    check("<html" in html and "</html>" in html, "html 标签闭合")
    check("<head>" in html and "</head>" in html, "head 标签闭合")
    check("<body>" in html and "</body>" in html, "body 标签闭合")

    print("-- 关键控件 id --")
    for i in REQUIRED_IDS:
        check(('id="%s"' % i) in html, "存在 id=%s" % i)

    print("-- 关键实现标记 --")
    for t in REQUIRED_TOKENS:
        check(t in html, "包含 " + t)

    # 脚本块括号配对（粗校验）
    scripts = re.findall(r"<script(?:\s[^>]*)?>(.*?)</script>", html, re.S)
    check(len(scripts) >= 2, "至少 2 个脚本块（库 + 业务）")
    biz = max(scripts, key=len)
    for left, right, name in [("{", "}", "花括号"), ("(", ")", "圆括号"), ("[", "]", "方括号")]:
        check(biz.count(left) == biz.count(right),
              "%s配对 (%d/%d)" % (name, biz.count(left), biz.count(right)))

    # 不应残留占位符
    check("__JSBARCODE_LIB__" not in html, "库占位符已替换（JsBarcode 已内嵌）")

    print()
    if failures:
        print("校验未通过，共 %d 项失败。" % len(failures))
        return 1
    print("全部校验通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
