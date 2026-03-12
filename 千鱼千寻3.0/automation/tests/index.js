const loginNeon = require('./logins/neon');
const loginGitHub = require('./logins/github');
const loginWechat = require('./logins/wechat');
const loginSupabase = require('./logins/supabase');
const loginVercel = require('./logins/vercel');
const loginFeishu = require('./logins/feishu');

/**
 * 批量登录所有网站
 */
async function loginAll() {
  console.log('🚀 开始批量登录...\n');

  const logins = [
    { name: 'Neon PostgreSQL', fn: loginNeon },
    { name: 'GitHub', fn: loginGitHub },
    { name: '微信公众平台', fn: loginWechat },
    { name: 'Supabase', fn: loginSupabase },
    { name: 'Vercel', fn: loginVercel },
    { name: '飞书', fn: loginFeishu },
  ];

  for (const login of logins) {
    console.log(`\n${'='.repeat(50)}`);
    console.log(`📌 登录: ${login.name}`);
    console.log('='.repeat(50));

    try {
      await login.fn();
      console.log(`✅ ${login.name} 登录完成\n`);
    } catch (error) {
      console.error(`❌ ${login.name} 登录失败:`, error.message, '\n');
    }

    // 等待 5 秒再登录下一个
    await new Promise(resolve => setTimeout(resolve, 5000));
  }

  console.log('\n🎉 所有登录任务完成！');
}

// 单独登录某个网站
async function loginSingle(siteName) {
  const sites = {
    neon: loginNeon,
    github: loginGitHub,
    wechat: loginWechat,
    supabase: loginSupabase,
    vercel: loginVercel,
    feishu: loginFeishu,
  };

  const loginFn = sites[siteName.toLowerCase()];
  if (!loginFn) {
    console.error(`❌ 未找到网站: ${siteName}`);
    console.log('可用的网站:', Object.keys(sites).join(', '));
    return;
  }

  await loginFn();
}

// 命令行参数处理
if (require.main === module) {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    // 没有参数，批量登录所有网站
    loginAll();
  } else {
    // 有参数，登录指定网站
    const siteName = args[0];
    loginSingle(siteName);
  }
}

module.exports = { loginAll, loginSingle };
