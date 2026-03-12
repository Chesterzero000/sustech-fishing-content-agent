const LoginHelper = require('../../utils/loginHelper');
require('dotenv').config();

/**
 * 飞书登录
 */
async function loginFeishu() {
  const helper = new LoginHelper();

  try {
    await helper.init();

    await helper.login({
      url: 'https://www.feishu.cn/login',
      usernameSelector: 'input[type="email"]',
      passwordSelector: 'input[type="password"]',
      submitSelector: 'button[type="submit"]',
      username: process.env.FEISHU_EMAIL,
      password: process.env.FEISHU_PASSWORD,
      waitForSelector: '.lark-header',
      afterSubmit: async (page) => {
        // 可能需要验证码
        const hasVerification = await page.$('input[placeholder*="验证码"]');
        if (hasVerification) {
          console.log('⚠️ 需要验证码，请手动输入');
          await page.waitForTimeout(60000);
        }
      },
    });

    await helper.saveCookies('./cookies/feishu.json');
    await helper.screenshot('./screenshots/feishu-success.png');
    await helper.page.waitForTimeout(30000);

  } catch (error) {
    console.error('❌ 登录失败:', error.message);
    await helper.screenshot('./screenshots/feishu-error.png');
  } finally {
    await helper.close();
  }
}

if (require.main === module) {
  loginFeishu();
}

module.exports = loginFeishu;
