const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

// 平台配置
const PLATFORMS = {
  github: {
    domain: 'github.com',
    cookieFile: 'github.json',
    loginScript: 'manual-login.js'
  },
  xiaohongshu: {
    domain: 'xiaohongshu.com',
    cookieFile: 'xiaohongshu.json',
    loginScript: 'tests/logins/xiaohongshu.js'
  },
  douyin: {
    domain: 'douyin.com',
    cookieFile: 'douyin.json',
    loginScript: 'tests/logins/douyin.js'
  },
  bilibili: {
    domain: 'bilibili.com',
    cookieFile: 'bilibili.json',
    loginScript: 'tests/logins/bilibili.js'
  }
};

// 识别平台
function identifyPlatform(url) {
  for (const [platform, config] of Object.entries(PLATFORMS)) {
    if (url.includes(config.domain)) {
      return platform;
    }
  }
  return null;
}

// 加载 Cookies
function loadCookies(platform) {
  const cookiePath = path.join(__dirname, 'cookies', PLATFORMS[platform].cookieFile);

  if (!fs.existsSync(cookiePath)) {
    return null;
  }

  try {
    const cookies = JSON.parse(fs.readFileSync(cookiePath, 'utf-8'));
    return cookies;
  } catch (error) {
    console.error(`❌ 加载 Cookies 失败:`, error.message);
    return null;
  }
}

// 验证 Cookies 是否有效
async function verifyCookies(platform, cookies) {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();

  try {
    await context.addCookies(cookies);
    const page = await context.newPage();

    // 根据平台访问不同的验证页面
    const testUrls = {
      github: 'https://github.com',
      xiaohongshu: 'https://www.xiaohongshu.com/explore',
      douyin: 'https://www.douyin.com/',
      bilibili: 'https://www.bilibili.com/'
    };

    await page.goto(testUrls[platform], { waitUntil: 'domcontentloaded', timeout: 10000 });
    await page.waitForTimeout(2000);

    // 检查是否登录成功
    const loginIndicators = {
      github: 'img[alt*="@"]',
      xiaohongshu: '.avatar',
      douyin: '.user-info, .avatar',
      bilibili: '.header-avatar'
    };

    const isLoggedIn = await page.$(loginIndicators[platform]);
    await browser.close();

    return !!isLoggedIn;
  } catch (error) {
    await browser.close();
    return false;
  }
}

// 自动登录
async function autoLogin(platform) {
  console.log(`🔐 正在登录 ${platform}...`);

  // 先尝试加载现有 Cookies
  let cookies = loadCookies(platform);

  if (cookies) {
    console.log(`📝 找到已保存的 Cookies，验证中...`);
    const isValid = await verifyCookies(platform, cookies);

    if (isValid) {
      console.log(`✅ Cookies 有效，已自动登录`);
      return cookies;
    } else {
      console.log(`⚠️ Cookies 已失效，需要重新登录`);
    }
  }

  // Cookies 不存在或失效，提示用户手动登录
  console.log(`❌ 需要手动登录 ${platform}`);
  console.log(`请运行: node ${PLATFORMS[platform].loginScript}`);
  return null;
}

// 提取 GitHub 仓库信息
async function extractGitHubRepo(page) {
  try {
    const title = await page.$eval('h1 strong a', el => el.textContent.trim()).catch(() => null);
    const description = await page.$eval('[data-pjax="#repo-content-pjax-container"] p', el => el.textContent.trim()).catch(() => null);

    const stats = await page.$$eval('.BorderGrid-cell', cells => {
      const result = {};
      cells.forEach(cell => {
        const text = cell.textContent.trim();
        if (text.includes('star')) result.stars = text.match(/[\d,]+/)?.[0] || '0';
        if (text.includes('fork')) result.forks = text.match(/[\d,]+/)?.[0] || '0';
        if (text.includes('watching')) result.watchers = text.match(/[\d,]+/)?.[0] || '0';
      });
      return result;
    }).catch(() => ({}));

    const languages = await page.$$eval('[data-ga-click*="language"]', els =>
      els.map(el => el.textContent.trim())
    ).catch(() => []);

    return {
      title,
      description,
      ...stats,
      languages
    };
  } catch (error) {
    console.error('提取 GitHub 信息失败:', error.message);
    return null;
  }
}

// 提取小红书笔记信息
async function extractXiaohongshuNote(page) {
  try {
    await page.waitForTimeout(3000);

    const title = await page.$eval('.title', el => el.textContent.trim()).catch(() => null);
    const content = await page.$eval('.content', el => el.textContent.trim()).catch(() => null);

    const stats = await page.$$eval('.interaction', els => {
      const result = {};
      els.forEach(el => {
        const text = el.textContent.trim();
        if (text.includes('点赞')) result.likes = text.match(/[\d.]+[万k]?/)?.[0] || '0';
        if (text.includes('收藏')) result.collects = text.match(/[\d.]+[万k]?/)?.[0] || '0';
        if (text.includes('评论')) result.comments = text.match(/[\d.]+[万k]?/)?.[0] || '0';
      });
      return result;
    }).catch(() => ({}));

    return {
      title,
      content,
      ...stats
    };
  } catch (error) {
    console.error('提取小红书信息失败:', error.message);
    return null;
  }
}

// 智能操作主函数
async function smartOperation(url, action = 'view', params = {}) {
  console.log('🚀 智能平台操作');
  console.log('==========================================');
  console.log('');

  // 1. 识别平台
  const platform = identifyPlatform(url);
  if (!platform) {
    console.error('❌ 无法识别平台');
    return { success: false, error: '不支持的平台' };
  }

  console.log(`📱 平台: ${platform}`);
  console.log(`🔗 链接: ${url}`);
  console.log(`⚡ 操作: ${action}`);
  console.log('');

  // 2. 自动登录
  const cookies = await autoLogin(platform);
  if (!cookies) {
    return { success: false, error: '登录失败' };
  }

  // 3. 执行操作
  const browser = await chromium.launch({
    headless: params.headless !== false,
    slowMo: 100
  });

  const context = await browser.newContext();
  await context.addCookies(cookies);

  const page = await context.newPage();

  try {
    console.log(`🌐 访问页面...`);
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(3000);

    let result = {};

    // 根据平台和操作执行不同的逻辑
    if (action === 'view') {
      console.log(`👀 提取内容...`);

      if (platform === 'github') {
        result = await extractGitHubRepo(page);
      } else if (platform === 'xiaohongshu') {
        result = await extractXiaohongshuNote(page);
      }

      console.log('');
      console.log('📊 提取结果:');
      console.log(JSON.stringify(result, null, 2));
    } else if (action === 'star' && platform === 'github') {
      console.log(`⭐ 点击 Star...`);
      const starButton = await page.$('button[data-ga-click*="star"]');
      if (starButton) {
        await starButton.click();
        await page.waitForTimeout(1000);
        console.log('✅ Star 成功');
        result = { success: true, action: 'starred' };
      } else {
        console.log('❌ 未找到 Star 按钮');
        result = { success: false, error: '未找到 Star 按钮' };
      }
    } else if (action === 'like' && (platform === 'xiaohongshu' || platform === 'douyin' || platform === 'bilibili')) {
      console.log(`👍 点击点赞...`);
      const likeButton = await page.$('.like-button, .like, [class*="like"]');
      if (likeButton) {
        await likeButton.click();
        await page.waitForTimeout(1000);
        console.log('✅ 点赞成功');
        result = { success: true, action: 'liked' };
      } else {
        console.log('❌ 未找到点赞按钮');
        result = { success: false, error: '未找到点赞按钮' };
      }
    }

    // 截图
    const screenshotPath = `./screenshots/${platform}-${action}-${Date.now()}.png`;
    await page.screenshot({ path: screenshotPath });
    console.log(`📸 截图已保存: ${screenshotPath}`);

    await browser.close();

    return {
      success: true,
      platform,
      action,
      url,
      data: result
    };

  } catch (error) {
    console.error('❌ 操作失败:', error.message);
    await page.screenshot({ path: `./screenshots/${platform}-error-${Date.now()}.png` }).catch(() => {});
    await browser.close();

    return {
      success: false,
      error: error.message
    };
  }
}

// 命令行接口
if (require.main === module) {
  const args = process.argv.slice(2);
  const url = args.find(arg => arg.startsWith('http'));
  const action = args.find(arg => arg.startsWith('--action='))?.split('=')[1] || 'view';
  const headless = !args.includes('--no-headless');

  if (!url) {
    console.error('❌ 请提供 URL');
    console.log('');
    console.log('使用方法:');
    console.log('  node smart-operation.js <url> [--action=view|star|like] [--no-headless]');
    console.log('');
    console.log('示例:');
    console.log('  node smart-operation.js https://github.com/user/repo');
    console.log('  node smart-operation.js https://github.com/user/repo --action=star');
    console.log('  node smart-operation.js https://www.xiaohongshu.com/explore/xxx --action=like');
    process.exit(1);
  }

  smartOperation(url, action, { headless }).then(result => {
    console.log('');
    console.log('==========================================');
    console.log('✅ 操作完成');
    console.log('');
    console.log('结果:', JSON.stringify(result, null, 2));
  }).catch(error => {
    console.error('❌ 错误:', error);
    process.exit(1);
  });
}

module.exports = { smartOperation, identifyPlatform, autoLogin };
