const { chromium } = require('playwright');
require('dotenv').config();

/**
 * 通用登录助手类
 */
class LoginHelper {
  constructor() {
    this.browser = null;
    this.context = null;
    this.page = null;
  }

  /**
   * 初始化浏览器
   */
  async init(options = {}) {
    this.browser = await chromium.launch({
      headless: options.headless || false,
      slowMo: options.slowMo || 100,
    });

    this.context = await this.browser.newContext({
      viewport: { width: 1280, height: 720 },
      userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    });

    this.page = await this.context.newPage();
    return this.page;
  }

  /**
   * 通用登录方法
   */
  async login(config) {
    const {
      url,
      usernameSelector,
      passwordSelector,
      submitSelector,
      username,
      password,
      waitForSelector,
      beforeSubmit,
      afterSubmit,
    } = config;

    console.log(`🔐 开始登录: ${url}`);

    // 访问登录页面
    await this.page.goto(url, { waitUntil: 'networkidle' });
    await this.page.waitForTimeout(2000);

    // 输入用户名
    console.log('📝 输入用户名...');
    await this.page.fill(usernameSelector, username);
    await this.page.waitForTimeout(500);

    // 输入密码
    console.log('🔑 输入密码...');
    await this.page.fill(passwordSelector, password);
    await this.page.waitForTimeout(500);

    // 提交前的自定义操作（如验证码）
    if (beforeSubmit) {
      console.log('⚙️ 执行提交前操作...');
      await beforeSubmit(this.page);
    }

    // 点击登录按钮
    console.log('🚀 点击登录按钮...');
    await this.page.click(submitSelector);

    // 等待登录成功
    if (waitForSelector) {
      console.log('⏳ 等待登录成功...');
      await this.page.waitForSelector(waitForSelector, { timeout: 30000 });
    } else {
      await this.page.waitForTimeout(5000);
    }

    // 提交后的自定义操作
    if (afterSubmit) {
      console.log('⚙️ 执行提交后操作...');
      await afterSubmit(this.page);
    }

    console.log('✅ 登录成功！');
    return this.page;
  }

  /**
   * 保存登录状态（Cookies）
   */
  async saveCookies(filepath) {
    const cookies = await this.context.cookies();
    const fs = require('fs');
    fs.writeFileSync(filepath, JSON.stringify(cookies, null, 2));
    console.log(`💾 Cookies 已保存到: ${filepath}`);
  }

  /**
   * 加载登录状态（Cookies）
   */
  async loadCookies(filepath) {
    const fs = require('fs');
    if (fs.existsSync(filepath)) {
      const cookies = JSON.parse(fs.readFileSync(filepath, 'utf-8'));
      await this.context.addCookies(cookies);
      console.log(`📂 Cookies 已加载: ${filepath}`);
      return true;
    }
    return false;
  }

  /**
   * 截图
   */
  async screenshot(filename) {
    await this.page.screenshot({ path: filename, fullPage: true });
    console.log(`📸 截图已保存: ${filename}`);
  }

  /**
   * 关闭浏览器
   */
  async close() {
    if (this.browser) {
      await this.browser.close();
      console.log('🔒 浏览器已关闭');
    }
  }

  /**
   * 等待用户手动操作（如验证码）
   */
  async waitForManualAction(message, timeout = 60000) {
    console.log(`⏸️ ${message}`);
    console.log(`⏱️ 等待 ${timeout / 1000} 秒...`);
    await this.page.waitForTimeout(timeout);
  }
}

module.exports = LoginHelper;
