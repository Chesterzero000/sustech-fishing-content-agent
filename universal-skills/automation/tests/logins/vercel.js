const LoginHelper = require('../../utils/loginHelper');
require('dotenv').config();

/**
 * Vercel 登录
 */
async function loginVercel() {
  const helper = new LoginHelper();

  try {
    await helper.init();

    await helper.login({
      url: 'https://vercel.com/login',
      usernameSelector: 'input[type="email"]',
      passwordSelector: 'input[type="password"]',
      submitSelector: 'button[type="submit"]',
      username: process.env.VERCEL_EMAIL,
      password: process.env.VERCEL_PASSWORD,
      waitForSelector: '[data-testid="dashboard-header"]',
    });

    await helper.saveCookies('./cookies/vercel.json');
    await helper.screenshot('./screenshots/vercel-success.png');
    await helper.page.waitForTimeout(30000);

  } catch (error) {
    console.error('❌ 登录失败:', error.message);
    await helper.screenshot('./screenshots/vercel-error.png');
  } finally {
    await helper.close();
  }
}

if (require.main === module) {
  loginVercel();
}

module.exports = loginVercel;
