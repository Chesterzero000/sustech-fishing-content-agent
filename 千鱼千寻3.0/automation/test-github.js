const { chromium } = require('playwright');
require('dotenv').config();

async function testGitHubLogin() {
  console.log('🧪 GitHub 登录测试');
  console.log('==================');
  console.log('');
  console.log('配置信息:');
  console.log(`用户名/邮箱: ${process.env.GITHUB_USERNAME}`);
  console.log(`密码: ${'*'.repeat(process.env.GITHUB_PASSWORD.length)}`);
  console.log('');

  const browser = await chromium.launch({
    headless: false,
    slowMo: 100,
  });

  const context = await browser.newContext();
  const page = await context.newPage();

  try {
    console.log('1️⃣ 访问 GitHub 登录页面...');
    await page.goto('https://github.com/login');
    await page.waitForTimeout(2000);

    console.log('2️⃣ 输入用户名/邮箱...');
    await page.fill('#login_field', process.env.GITHUB_USERNAME);
    await page.waitForTimeout(1000);

    console.log('3️⃣ 输入密码...');
    await page.fill('#password', process.env.GITHUB_PASSWORD);
    await page.waitForTimeout(1000);

    console.log('4️⃣ 点击登录按钮...');
    await page.click('input[type="submit"]');

    console.log('5️⃣ 等待响应...');
    await page.waitForTimeout(5000);

    // 检查错误
    const errorElement = await page.$('.flash-error');
    if (errorElement) {
      const errorText = await errorElement.textContent();
      console.log('');
      console.log('❌ 登录失败！');
      console.log('错误信息:', errorText.trim());
      console.log('');
      console.log('可能的原因:');
      console.log('1. 用户名或密码错误');
      console.log('2. GitHub 账号不存在');
      console.log('3. 需要验证码');
      console.log('');
      console.log('建议:');
      console.log('1. 检查邮箱是否正确: hc3571591632@qq.com');
      console.log('2. 检查密码是否正确');
      console.log('3. 尝试在浏览器中手动登录一次');
    } else {
      // 检查是否有验证码
      const hasCaptcha = await page.$('[data-hcaptcha-widget-id]');
      if (hasCaptcha) {
        console.log('⚠️ 需要验证码！');
        console.log('请在浏览器中完成验证码，然后按回车继续...');
        await page.waitForTimeout(60000);
      }

      // 检查是否需要 2FA
      const has2FA = await page.$('input[name="otp"]');
      if (has2FA) {
        console.log('⚠️ 需要双因素认证！');
        console.log('请在浏览器中输入验证码，然后按回车继续...');
        await page.waitForTimeout(60000);
      }

      // 检查是否登录成功
      const avatar = await page.$('img[alt*="@"]');
      if (avatar) {
        console.log('');
        console.log('✅ 登录成功！');
        console.log('');

        // 保存 Cookies
        const cookies = await context.cookies();
        const fs = require('fs');
        fs.writeFileSync('./cookies/github.json', JSON.stringify(cookies, null, 2));
        console.log('💾 Cookies 已保存到: ./cookies/github.json');

        // 截图
        await page.screenshot({ path: './screenshots/github-success.png', fullPage: true });
        console.log('📸 截图已保存到: ./screenshots/github-success.png');
      } else {
        console.log('⚠️ 无法确认登录状态');
        console.log('浏览器将保持打开，请手动检查');
      }
    }

    console.log('');
    console.log('⏱️ 浏览器将在 30 秒后关闭...');
    await page.waitForTimeout(30000);

  } catch (error) {
    console.error('❌ 测试失败:', error.message);
  } finally {
    await browser.close();
    console.log('🔒 浏览器已关闭');
  }
}

testGitHubLogin();
