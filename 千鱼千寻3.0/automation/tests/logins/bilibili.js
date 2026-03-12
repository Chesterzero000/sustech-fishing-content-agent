const { chromium } = require('playwright');
require('dotenv').config();

async function loginBilibili() {
  console.log('🔐 开始登录 B站');

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
    console.log('1️⃣ 访问 B站登录页面...');
    await page.goto('https://passport.bilibili.com/login', {
      waitUntil: 'domcontentloaded',
      timeout: 60000
    });
    await page.waitForTimeout(3000);

    console.log('');
    console.log('⚠️ 请注意浏览器窗口！');
    console.log('');
    console.log('B站登录方式：');
    console.log('1. 扫码登录（推荐）- 使用 B站 App 扫码');
    console.log('2. 账号密码登录 - 输入账号密码');
    console.log('3. 短信登录 - 输入手机号和验证码');
    console.log('');
    console.log('⏱️ 脚本将等待 120 秒供你完成登录...');
    console.log('');

    // 等待用户手动登录
    await page.waitForTimeout(120000);

    // 检查登录状态
    console.log('🔍 检查登录状态...');
    const currentUrl = page.url();
    console.log('当前 URL:', currentUrl);

    // 如果跳转到首页，说明登录成功
    if (currentUrl.includes('bilibili.com') && !currentUrl.includes('login')) {
      console.log('✅ 登录成功！');

      // 保存 Cookies
      const cookies = await context.cookies();
      const fs = require('fs');
      fs.mkdirSync('./cookies', { recursive: true });
      fs.writeFileSync('./cookies/bilibili.json', JSON.stringify(cookies, null, 2));
      console.log('💾 Cookies 已保存到: ./cookies/bilibili.json');

      // 截图
      await page.screenshot({ path: './screenshots/bilibili-success.png', fullPage: true });
      console.log('📸 截图已保存到: ./screenshots/bilibili-success.png');

      console.log('');
      console.log('✅ 完成！下次可以使用保存的 Cookies 自动登录');
    } else {
      console.log('⚠️ 无法确认登录状态，但已保存当前 Cookies');

      // 仍然保存 Cookies
      const cookies = await context.cookies();
      const fs = require('fs');
      fs.mkdirSync('./cookies', { recursive: true });
      fs.writeFileSync('./cookies/bilibili.json', JSON.stringify(cookies, null, 2));
      console.log('💾 Cookies 已保存到: ./cookies/bilibili.json');

      await page.screenshot({ path: './screenshots/bilibili-manual.png', fullPage: true });
      console.log('📸 截图已保存到: ./screenshots/bilibili-manual.png');
    }

    console.log('');
    console.log('⏱️ 浏览器将在 10 秒后关闭...');
    await page.waitForTimeout(10000);

  } catch (error) {
    console.error('❌ 错误:', error.message);
    await page.screenshot({ path: './screenshots/bilibili-error.png' }).catch(() => {});
  } finally {
    await browser.close();
    console.log('🔒 浏览器已关闭');
  }
}

loginBilibili();
