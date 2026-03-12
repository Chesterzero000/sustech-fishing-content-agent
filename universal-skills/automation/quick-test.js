const { chromium } = require('playwright');
require('dotenv').config();

async function quickTestGitHub() {
  console.log('🧪 快速测试 GitHub 连接');
  console.log('==================');
  console.log('');

  const browser = await chromium.launch({
    headless: false,
    slowMo: 100,
  });

  const context = await browser.newContext();
  const page = await context.newPage();

  try {
    console.log('1️⃣ 测试访问 GitHub...');

    // 设置更长的超时时间
    page.setDefaultTimeout(60000);

    await page.goto('https://github.com/login', {
      waitUntil: 'domcontentloaded',
      timeout: 60000
    });

    console.log('✅ 成功访问 GitHub 登录页面');
    console.log('');

    console.log('2️⃣ 输入账号信息...');
    await page.fill('#login_field', process.env.GITHUB_USERNAME);
    await page.waitForTimeout(1000);

    await page.fill('#password', process.env.GITHUB_PASSWORD);
    await page.waitForTimeout(1000);

    console.log('3️⃣ 点击登录...');
    await page.click('input[type="submit"]');

    console.log('4️⃣ 等待响应...');
    await page.waitForTimeout(10000);

    // 检查错误
    const errorElement = await page.$('.flash-error');
    if (errorElement) {
      const errorText = await errorElement.textContent();
      console.log('❌ 登录失败:', errorText.trim());
    } else {
      console.log('✅ 没有发现错误提示');

      // 检查是否登录成功
      const avatar = await page.$('img[alt*="@"]');
      if (avatar) {
        console.log('✅ 登录成功！');

        // 保存 Cookies
        const cookies = await context.cookies();
        const fs = require('fs');
        fs.writeFileSync('./cookies/github.json', JSON.stringify(cookies, null, 2));
        console.log('💾 Cookies 已保存');

        await page.screenshot({ path: './screenshots/github-success.png' });
        console.log('📸 截图已保存');
      }
    }

    console.log('');
    console.log('⏱️ 浏览器将在 30 秒后关闭...');
    await page.waitForTimeout(30000);

  } catch (error) {
    console.error('❌ 错误:', error.message);

    if (error.message.includes('ERR_CONNECTION')) {
      console.log('');
      console.log('⚠️ 网络连接问题！');
      console.log('');
      console.log('可能的原因:');
      console.log('1. GitHub 访问受限（需要代理）');
      console.log('2. 网络不稳定');
      console.log('3. 防火墙阻止');
      console.log('');
      console.log('解决方案:');
      console.log('1. 检查网络连接');
      console.log('2. 尝试使用代理');
      console.log('3. 在浏览器中手动访问 https://github.com 测试');
    }

    await page.screenshot({ path: './screenshots/github-error.png' }).catch(() => {});
  } finally {
    await browser.close();
    console.log('🔒 浏览器已关闭');
  }
}

quickTestGitHub();
