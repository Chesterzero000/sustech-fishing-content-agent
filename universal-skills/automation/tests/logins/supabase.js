const LoginHelper = require('../../utils/loginHelper');
require('dotenv').config();

/**
 * Supabase 登录
 */
async function loginSupabase() {
  const helper = new LoginHelper();

  try {
    await helper.init();

    await helper.login({
      url: 'https://supabase.com/dashboard/sign-in',
      usernameSelector: 'input[type="email"]',
      passwordSelector: 'input[type="password"]',
      submitSelector: 'button[type="submit"]',
      username: process.env.SUPABASE_EMAIL,
      password: process.env.SUPABASE_PASSWORD,
      waitForSelector: '[data-testid="dashboard-header"]',
    });

    await helper.saveCookies('./cookies/supabase.json');
    await helper.screenshot('./screenshots/supabase-success.png');
    await helper.page.waitForTimeout(30000);

  } catch (error) {
    console.error('❌ 登录失败:', error.message);
    await helper.screenshot('./screenshots/supabase-error.png');
  } finally {
    await helper.close();
  }
}

if (require.main === module) {
  loginSupabase();
}

module.exports = loginSupabase;
