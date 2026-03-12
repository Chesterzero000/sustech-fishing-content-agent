const { chromium } = require('playwright');
require('dotenv').config();

async function loginDouyin() {
  console.log('🔐 开始登录抖音');

  const browser = await chromium.launch({
    headless: false,
    slowMo: 500,
  });

  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 },
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  });

  const page = await context.newPage();

  try {
    console.log('1️⃣ 访问抖音网页版...');
    await page.goto('https://www.douyin.com/', {
      waitUntil: 'domcontentloaded',
      timeout: 60000
    });
    await page.waitForTimeout(3000);

    console.log('');
    console.log('⚠️ 请注意浏览器窗口！');
    console.log('');
    console.log('抖音登录方式：');
    console.log('1. 扫码登录（推荐）- 使用抖音 App 扫码');
    console.log('2. 手机号登录 - 输入手机号和验证码');
    console.log('');
    console.log('⏱️ 脚本将等待 120 秒供你完成登录...');
    console.log('');

    // 等待用户手动登录
    await page.waitForTimeout(120000);

    // 检查登录状态
    console.log('🔍 检查登录状态...');
    const currentUrl = page.url();
    console.log('当前 URL:', currentUrl);

    // 检查是否有用户信息（登录成功的标志）
    const userInfo = await page.$('.user-info, .avatar');
    if (userInfo) {
      console.log('✅ 登录成功！');

      // 保存 Cookies
      const cookies = await context.cookies();
      const fs = require('fs');
      fs.mkdirSync('./cookies', { recursive: true });
      fs.writeFileSync('./cookies/douyin.json', JSON.stringify(cookies, null, 2));
      console.log('💾 Cookies 已保存到: ./cookies/douyin.json');

      // 截图
      await page.screenshot({ path: './screenshots/douyin-success.png', fullPage: true });
      console.log('📸 截图已保存到: ./screenshots/douyin-success.png');

      console.log('');
      console.log('✅ 完成！下次可以使用保存的 Cookies 自动登录');
    } else {
      console.log('⚠️ 无法确认登录状态，但已保存当前 Cookies');

      // 仍然保存 Cookies
      const cookies = await context.cookies();
      const fs = require('fs');
      fs.mkdirSync('./cookies', { recursive: true });
      fs.writeFileSync('./cookies/douyin.json', JSON.stringify(cookies, null, 2));
      console.log('💾 Cookies 已保存到: ./cookies/douyin.json');

      await page.screenshot({ path: './screenshots/douyin-manual.png', fullPage: true });
      console.log('📸 截图已保存到: ./screenshots/douyin-manual.png');
    }

    console.log('');
    console.log('⏱️ 浏览器将在 10 秒后关闭...');
    await page.waitForTimeout(10000);

  } catch (error) {
    console.error('❌ 错误:', error.message);
    await page.screenshot({ path: './screenshots/douyin-error.png' }).catch(() => {});
  } finally {
    await browser.close();
    console.log('🔒 浏览器已关闭');
  }
}

loginDouyin();
