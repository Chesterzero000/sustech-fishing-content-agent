const LoginHelper = require('../../utils/loginHelper');
require('dotenv').config();

/**
 * 微信公众平台登录
 */
async function loginWechat() {
  const helper = new LoginHelper();

  try {
    await helper.init();

    console.log('🔐 开始登录微信公众平台');
    await helper.page.goto('https://mp.weixin.qq.com/', { waitUntil: 'networkidle' });
    await helper.page.waitForTimeout(3000);

    // 微信公众平台使用扫码登录
    console.log('📱 请使用微信扫描二维码登录');
    console.log('⏱️ 等待 60 秒...');

    // 等待用户扫码
    await helper.page.waitForSelector('.weui-desktop-account__nickname', { timeout: 60000 });

    console.log('✅ 登录成功！');

    await helper.saveCookies('./cookies/wechat.json');
    await helper.screenshot('./screenshots/wechat-success.png');
    await helper.page.waitForTimeout(30000);

  } catch (error) {
    console.error('❌ 登录失败:', error.message);
    await helper.screenshot('./screenshots/wechat-error.png');
  } finally {
    await helper.close();
  }
}

if (require.main === module) {
  loginWechat();
}

module.exports = loginWechat;
