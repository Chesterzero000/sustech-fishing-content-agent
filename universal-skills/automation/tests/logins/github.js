const LoginHelper = require('../../utils/loginHelper');
require('dotenv').config();

/**
 * GitHub 登录
 */
async function loginGitHub() {
  const helper = new LoginHelper();

  try {
    await helper.init();

    console.log('🔐 开始登录 GitHub');
    await helper.page.goto('https://github.com/login', { waitUntil: 'networkidle' });
    await helper.page.waitForTimeout(2000);

    // 输入用户名
    console.log('📝 输入用户名...');
    await helper.page.fill('#login_field', process.env.GITHUB_USERNAME);
    await helper.page.waitForTimeout(500);

    // 输入密码
    console.log('🔑 输入密码...');
    await helper.page.fill('#password', process.env.GITHUB_PASSWORD);
    await helper.page.waitForTimeout(500);

    // 点击登录按钮
    console.log('🚀 点击登录按钮...');
    await helper.page.click('input[type="submit"]');

    // 等待页面跳转
    console.log('⏳ 等待页面响应...');
    await helper.page.waitForTimeout(5000);

    // 检查是否有错误提示
    const errorMsg = await helper.page.$('.flash-error');
    if (errorMsg) {
      const errorText = await errorMsg.textContent();
      console.log('❌ 登录错误:', errorText);
      await helper.screenshot('./screenshots/github-error.png');
      return;
    }

    // 检查是否需要验证码
    const hasCaptcha = await helper.page.$('[data-hcaptcha-widget-id]');
    if (hasCaptcha) {
      console.log('⚠️ 需要验证码，请手动完成验证');
      console.log('⏱️ 等待 60 秒...');
      await helper.page.waitForTimeout(60000);
    }

    // 检查是否需要双因素认证
    const has2FA = await helper.page.$('input[name="otp"]');
    if (has2FA) {
      console.log('⚠️ 需要双因素认证，请手动输入验证码');
      console.log('⏱️ 等待 60 秒...');
      await helper.page.waitForTimeout(60000);
    }

    // 检查是否登录成功（多个可能的选择器）
    console.log('🔍 检查登录状态...');
    const selectors = [
      '[data-test-selector="nav-avatar"]',
      'img[alt*="@"]',
      '.Header-link[href*="/settings"]',
      'summary[aria-label*="View profile"]'
    ];

    let loginSuccess = false;
    for (const selector of selectors) {
      const element = await helper.page.$(selector);
      if (element) {
        console.log(`✅ 登录成功！(找到元素: ${selector})`);
        loginSuccess = true;
        break;
      }
    }

    if (!loginSuccess) {
      console.log('⚠️ 无法确认登录状态，保持浏览器打开 30 秒供你检查');
      await helper.page.waitForTimeout(30000);
    }

    await helper.saveCookies('./cookies/github.json');
    await helper.screenshot('./screenshots/github-success.png');

    console.log('💾 Cookies 已保存');
    console.log('📸 截图已保存');
    console.log('⏱️ 浏览器将在 30 秒后关闭...');
    await helper.page.waitForTimeout(30000);

  } catch (error) {
    console.error('❌ 登录失败:', error.message);
    await helper.screenshot('./screenshots/github-error.png');
    console.log('📸 错误截图已保存: ./screenshots/github-error.png');
    console.log('⏱️ 浏览器将在 10 秒后关闭，请查看截图...');
    await helper.page.waitForTimeout(10000);
  } finally {
    await helper.close();
  }
}

if (require.main === module) {
  loginGitHub();
}

module.exports = loginGitHub;
