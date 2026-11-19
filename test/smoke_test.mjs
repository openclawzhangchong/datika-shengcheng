/**
 * 冒烟测试（Node，无第三方 require 依赖）：
 * 用 npx playwright screenshot 对 index.html 截图，确认页面能正常渲染。
 * 依赖：npx playwright install chromium（首次）
 * 用法：node test/smoke_test.mjs
 */
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import path from "node:path";
import fs from "node:fs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, "..");
const html = path.join(root, "index.html");
const shotDir = path.join(__dirname, "screenshots");
fs.mkdirSync(shotDir, { recursive: true });

const out = path.join(shotDir, "smoke.png");
const fileUrl = "file:///" + html.replace(/\\/g, "/");

let ok = true;
function check(cond, msg) {
  console.log(`  [${cond ? "OK" : "FAIL"}] ${msg}`);
  if (!cond) ok = false;
}

console.log("== 冒烟测试 ==");
// Windows 下 npx 是 npx.cmd，用 execSync + shell 跨平台更稳
import { execSync } from "node:child_process";
try {
  const cmd = `npx playwright screenshot --viewport-size=900,1200 --wait-for-timeout=1000 "${fileUrl}" "${out}"`;
  execSync(cmd, { stdio: "pipe", cwd: root, shell: true });
  check(fs.existsSync(out), "截图生成成功");
  const size = fs.existsSync(out) ? fs.statSync(out).size : 0;
  check(size > 10000, `截图文件大小合理（${size} 字节）`);
} catch (e) {
  check(false, "Playwright 截图执行：" + (e.stderr?.toString().slice(0, 200) || e.message));
}

process.exit(ok ? 0 : 1);
