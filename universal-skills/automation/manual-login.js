const { chromium } = require('playwright');
require('dotenv').config();

async function manualGitHubLogin() {
  console.log('🔐 GitHub 手动辅助登录');
  console.log('==================');
  console.log('');
  console.log('这个脚本会帮你填写账号密码，但需要你手动完成验证');
  console.log('');

  const browser = await chromium.launch({
    headless: false,
    slowMo: 500, // 慢速操作，更像人类
  });

  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 },
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  });

  const page = await context.newPage();

  try {
    console.log('1️⃣ 访问 GitHub 登录页面...');
    await page.goto('https://github.com/login', {
      waitUntil: 'domcontentloaded',
      timeout: 60000
    });
    await page.waitForTimeout(3000);

    console.log('2️⃣ 填写账号: ' + process.env.GITHUB_USERNAME);
    await page.type('#login_field', process.env.GITHUB_USERNAME, { delay: 100 });
    await page.waitForTimeout(1000);

    console.log('3️⃣ 填写密码...');
    await page.type('#password', process.env.GITHUB_PASSWORD, { delay: 100 });
    await page.waitForTimeout(1000);

    console.log('');
    console.log('⚠️ 请注意浏览器窗口！');
    console.log('');
    console.log('接下来请手动操作：');
    console.log('1. 如果有验证码，请完成验证');
    console.log('2. 点击 "Sign in" 按钮');
    console.log('3. 如果需要双因素认证，请输入验证码');
    console.log('');
    console.log('⏱️ 脚本将等待 120 秒...');
    console.log('');

    // 等待 2 分钟让用户手动操作
    await page.waitForTimeout(120000);

    // 检查是否登录成功
    console.log('🔍 检查登录状态...');

    const currentUrl = page.url();
    console.log('当前 URL:', currentUrl);

    if (currentUrl.includes('github.com') && !currentUrl.includes('/login')) {
      console.log('✅ 看起来登录成功了！');

      // 保存 Cookies
      const cookies = await context.cookies();
      const fs = require('fs');
      fs.mkdirSync('./cookies', { recursive: true });
      fs.writeFileSync('./cookies/github.json', JSON.stringify(cookies, null, 2));
      console.log('💾 Cookies 已保存到: ./cookies/github.json');

      // 截图
      await page.screenshot({ path: './screenshots/github-success.png', fullPage: true });
      console.log('📸 截图已保存到: ./screenshots/github-success.png');

      console.log('');
      console.log('✅ 完成！下次可以使用保存的 Cookies 自动登录');
    } else {
      console.log('⚠️ 无法确认登录状态');
      await page.screenshot({ path: './screenshots/github-manual.png', fullPage: true });
      console.log('📸 截图已保存到: ./screenshots/github-manual.png');
    }

    console.log('');
    console.log('⏱️ 浏览器将在 10 秒后关闭...');
    await page.waitForTimeout(10000);

  } catch (error) {
    console.error('❌ 错误:', error.message);
  } finally {
    await browser.close();
    console.log('🔒 浏览器已关闭');
  }
}

manualGitHubLogin();
