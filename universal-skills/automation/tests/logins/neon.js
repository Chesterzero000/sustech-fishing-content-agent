const LoginHelper = require('../../utils/loginHelper');
require('dotenv').config();

/**
 * Neon PostgreSQL 登录
 */
async function loginNeon() {
  const helper = new LoginHelper();

  try {
    await helper.init();

    await helper.login({
      url: 'https://console.neon.tech/sign_in',
      usernameSelector: 'input[type="email"]',
      passwordSelector: 'input[type="password"]',
      submitSelector: 'button[type="submit"]',
      username: process.env.NEON_EMAIL,
      password: process.env.NEON_PASSWORD,
      waitForSelector: '[data-testid="projects-list"]',
    });

    // 保存登录状态
    await helper.saveCookies('./cookies/neon.json');
    await helper.screenshot('./screenshots/neon-success.png');

    // 保持浏览器打开 30 秒，方便查看
    await helper.page.waitForTimeout(30000);

  } catch (error) {
    console.error('❌ 登录失败:', error.message);
    await helper.screenshot('./screenshots/neon-error.png');
  } finally {
    await helper.close();
  }
}

// 如果直接运行此文件
if (require.main === module) {
  loginNeon();
}

module.exports = loginNeon;
