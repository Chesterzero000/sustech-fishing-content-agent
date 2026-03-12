const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// 平台配置
const platforms = [
  { name: 'GitHub', cookieFile: 'github.json', testUrl: 'https://github.com', loginIndicator: 'img[alt*="@"]' },
  { name: '小红书', cookieFile: 'xiaohongshu.json', testUrl: 'https://www.xiaohongshu.com/explore', loginIndicator: '.avatar' },
  { name: '抖音', cookieFile: 'douyin.json', testUrl: 'https://www.douyin.com/', loginIndicator: '.user-info, .avatar' },
  { name: 'B站', cookieFile: 'bilibili.json', testUrl: 'https://www.bilibili.com/', loginIndicator: '.header-avatar' },
];

async function verifyCookies(platform) {
  const cookiePath = path.join(__dirname, 'cookies', platform.cookieFile);

  // 检查 Cookie 文件是否存在
  if (!fs.existsSync(cookiePath)) {
    return {
      platform: platform.name,
      exists: false,
      valid: false,
      message: 'Cookie 文件不存在'
    };
  }

  // 读取 Cookies
  const cookies = JSON.parse(fs.readFileSync(cookiePath, 'utf-8'));

  // 检查 Cookie 是否为空
  if (!cookies || cookies.length === 0) {
    return {
      platform: platform.name,
      exists: true,
      valid: false,
      message: 'Cookie 文件为空'
    };
  }

  // 使用 Playwright 验证 Cookies
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();

  try {
    // 加载 Cookies
    await context.addCookies(cookies);

    const page = await context.newPage();
    await page.goto(platform.testUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(3000);

    // 检查登录状态
    const loginElement = await page.$(platform.loginIndicator);

    await browser.close();

    if (loginElement) {
      return {
        platform: platform.name,
        exists: true,
        valid: true,
        message: '登录状态有效',
        cookieCount: cookies.length
      };
    } else {
      return {
        platform: platform.name,
        exists: true,
        valid: false,
        message: '登录状态已失效',
        cookieCount: cookies.length
      };
    }
  } catch (error) {
    await browser.close();
    return {
      platform: platform.name,
      exists: true,
      valid: false,
      message: `验证失败: ${error.message}`,
      cookieCount: cookies.length
    };
  }
}

async function verifyAllCookies() {
  console.log('🍪 开始验证所有平台的 Cookies');
  console.log('==========================================');
  console.log('');

  const results = [];

  for (const platform of platforms) {
    console.log(`📝 验证 ${platform.name}...`);
    const result = await verifyCookies(platform);
    results.push(result);

    const statusIcon = result.valid ? '✅' : '❌';
    console.log(`${statusIcon} ${result.platform}: ${result.message}`);
    if (result.cookieCount) {
      console.log(`   Cookie 数量: ${result.cookieCount}`);
    }
    console.log('');
  }

  // 生成报告
  console.log('==========================================');
  console.log('📊 验证报告');
  console.log('==========================================');
  console.log('');

  const validCount = results.filter(r => r.valid).length;
  const invalidCount = results.filter(r => !r.valid).length;

  console.log(`总平台数: ${results.length}`);
  console.log(`✅ 有效: ${validCount}`);
  console.log(`❌ 无效: ${invalidCount}`);
  console.log('');

  if (invalidCount > 0) {
    console.log('需要重新登录的平台:');
    results.filter(r => !r.valid).forEach(r => {
      console.log(`  - ${r.platform}: ${r.message}`);
    });
    console.log('');
  }

  // 保存报告
  const reportPath = path.join(__dirname, 'cookie-verification-report.json');
  const reportData = {
    timestamp: new Date().toISOString(),
    summary: {
      total: results.length,
      valid: validCount,
      invalid: invalidCount
    },
    results
  };

  fs.writeFileSync(reportPath, JSON.stringify(reportData, null, 2));
  console.log(`📄 验证报告已保存到: ${reportPath}`);
  console.log('');
  console.log('✅ 验证完成！');
}

// 运行验证
verifyAllCookies().catch(error => {
  console.error('❌ 验证过程出错:', error);
  process.exit(1);
});
