const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

/**
 * CLI Anything 风格的自动包装器
 * 自动将任何网站转换为可操作的 CLI 接口
 */

class CLIAnythingWrapper {
  constructor(options = {}) {
    this.headless = options.headless !== false;
    this.slowMo = options.slowMo || 100;
    this.timeout = options.timeout || 30000;
  }

  /**
   * 自动分析网站结构
   */
  async analyzeWebsite(url) {
    console.log(`🔍 分析网站结构: ${url}`);

    const browser = await chromium.launch({ headless: this.headless });
    const page = await browser.newPage();

    try {
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: this.timeout });
      await page.waitForTimeout(2000);

      // 提取所有可交互元素
      const interactiveElements = await page.evaluate(() => {
        const elements = [];

        // 按钮
        document.querySelectorAll('button, [role="button"], .btn, .button').forEach((el, index) => {
          elements.push({
            type: 'button',
            text: el.textContent.trim(),
            selector: `button:nth-of-type(${index + 1})`,
            id: el.id,
            class: el.className
          });
        });

        // 链接
        document.querySelectorAll('a[href]').forEach((el, index) => {
          elements.push({
            type: 'link',
            text: el.textContent.trim(),
            href: el.href,
            selector: `a:nth-of-type(${index + 1})`
          });
        });

        // 输入框
        document.querySelectorAll('input, textarea').forEach((el, index) => {
          elements.push({
            type: 'input',
            inputType: el.type,
            placeholder: el.placeholder,
            name: el.name,
            selector: `input:nth-of-type(${index + 1})`
          });
        });

        // 下拉框
        document.querySelectorAll('select').forEach((el, index) => {
          elements.push({
            type: 'select',
            name: el.name,
            options: Array.from(el.options).map(opt => opt.text),
            selector: `select:nth-of-type(${index + 1})`
          });
        });

        return elements;
      });

      await browser.close();

      return {
        url,
        elements: interactiveElements,
        timestamp: new Date().toISOString()
      };

    } catch (error) {
      await browser.close();
      throw error;
    }
  }

  /**
   * 生成 CLI 命令
   */
  generateCLICommands(analysis) {
    const commands = [];

    analysis.elements.forEach((element, index) => {
      if (element.type === 'button') {
        commands.push({
          command: `click-button-${index}`,
          description: `点击按钮: ${element.text}`,
          selector: element.selector,
          action: 'click'
        });
      } else if (element.type === 'link') {
        commands.push({
          command: `click-link-${index}`,
          description: `点击链接: ${element.text}`,
          selector: element.selector,
          action: 'click'
        });
      } else if (element.type === 'input') {
        commands.push({
          command: `fill-input-${index}`,
          description: `填写输入框: ${element.placeholder || element.name}`,
          selector: element.selector,
          action: 'fill',
          params: ['value']
        });
      } else if (element.type === 'select') {
        commands.push({
          command: `select-option-${index}`,
          description: `选择选项: ${element.name}`,
          selector: element.selector,
          action: 'select',
          params: ['option']
        });
      }
    });

    return commands;
  }

  /**
   * 执行 CLI 命令
   */
  async executeCommand(url, command, params = {}) {
    console.log(`⚡ 执行命令: ${command.command}`);

    const browser = await chromium.launch({ headless: this.headless, slowMo: this.slowMo });
    const page = await browser.newPage();

    try {
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: this.timeout });
      await page.waitForTimeout(2000);

      const element = await page.$(command.selector);
      if (!element) {
        throw new Error(`未找到元素: ${command.selector}`);
      }

      if (command.action === 'click') {
        await element.click();
        console.log(`✅ 点击成功: ${command.description}`);
      } else if (command.action === 'fill') {
        await element.fill(params.value || '');
        console.log(`✅ 填写成功: ${command.description}`);
      } else if (command.action === 'select') {
        await element.selectOption(params.option || '');
        console.log(`✅ 选择成功: ${command.description}`);
      }

      await page.waitForTimeout(2000);

      // 截图
      const screenshotPath = `./screenshots/cli-anything-${Date.now()}.png`;
      await page.screenshot({ path: screenshotPath });
      console.log(`📸 截图已保存: ${screenshotPath}`);

      await browser.close();

      return {
        success: true,
        command: command.command,
        description: command.description
      };

    } catch (error) {
      await browser.close();
      throw error;
    }
  }

  /**
   * 包装网站为 CLI
   */
  async wrapWebsite(url, outputPath = null) {
    console.log('🎁 CLI Anything - 自动包装网站');
    console.log('==========================================');
    console.log('');

    // 1. 分析网站
    console.log('📊 步骤 1: 分析网站结构...');
    const analysis = await this.analyzeWebsite(url);
    console.log(`✅ 找到 ${analysis.elements.length} 个可交互元素`);
    console.log('');

    // 2. 生成 CLI 命令
    console.log('🔧 步骤 2: 生成 CLI 命令...');
    const commands = this.generateCLICommands(analysis);
    console.log(`✅ 生成 ${commands.length} 个 CLI 命令`);
    console.log('');

    // 3. 保存配置
    const config = {
      url,
      analysis,
      commands,
      createdAt: new Date().toISOString()
    };

    const configPath = outputPath || `./cli-wrappers/${this.sanitizeFilename(url)}.json`;
    fs.mkdirSync(path.dirname(configPath), { recursive: true });
    fs.writeFileSync(configPath, JSON.stringify(config, null, 2));

    console.log(`💾 配置已保存: ${configPath}`);
    console.log('');

    // 4. 显示可用命令
    console.log('📋 可用命令:');
    commands.slice(0, 10).forEach(cmd => {
      console.log(`  - ${cmd.command}: ${cmd.description}`);
    });

    if (commands.length > 10) {
      console.log(`  ... 还有 ${commands.length - 10} 个命令`);
    }

    console.log('');
    console.log('==========================================');
    console.log('✅ 包装完成！');
    console.log('');
    console.log('使用方法:');
    console.log(`  node cli-anything-wrapper.js --execute ${configPath} --command <command-name>`);

    return config;
  }

  /**
   * 从配置文件执行命令
   */
  async executeFromConfig(configPath, commandName, params = {}) {
    const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
    const command = config.commands.find(cmd => cmd.command === commandName);

    if (!command) {
      throw new Error(`未找到命令: ${commandName}`);
    }

    return await this.executeCommand(config.url, command, params);
  }

  /**
   * 清理文件名
   */
  sanitizeFilename(url) {
    return url.replace(/[^a-z0-9]/gi, '-').toLowerCase();
  }
}

// 命令行接口
if (require.main === module) {
  const args = process.argv.slice(2);

  if (args.includes('--wrap')) {
    // 包装网站
    const urlIndex = args.indexOf('--wrap') + 1;
    const url = args[urlIndex];

    if (!url) {
      console.error('❌ 请提供 URL');
      console.log('使用方法: node cli-anything-wrapper.js --wrap <url>');
      process.exit(1);
    }

    const wrapper = new CLIAnythingWrapper();
    wrapper.wrapWebsite(url).catch(error => {
      console.error('❌ 错误:', error.message);
      process.exit(1);
    });

  } else if (args.includes('--execute')) {
    // 执行命令
    const configIndex = args.indexOf('--execute') + 1;
    const configPath = args[configIndex];

    const commandIndex = args.indexOf('--command') + 1;
    const commandName = args[commandIndex];

    if (!configPath || !commandName) {
      console.error('❌ 请提供配置文件和命令名称');
      console.log('使用方法: node cli-anything-wrapper.js --execute <config> --command <command-name>');
      process.exit(1);
    }

    const wrapper = new CLIAnythingWrapper();
    wrapper.executeFromConfig(configPath, commandName).then(result => {
      console.log('✅ 执行成功:', result);
    }).catch(error => {
      console.error('❌ 错误:', error.message);
      process.exit(1);
    });

  } else {
    console.log('CLI Anything Wrapper - 自动包装任何网站为 CLI');
    console.log('');
    console.log('使用方法:');
    console.log('  包装网站:');
    console.log('    node cli-anything-wrapper.js --wrap <url>');
    console.log('');
    console.log('  执行命令:');
    console.log('    node cli-anything-wrapper.js --execute <config> --command <command-name>');
    console.log('');
    console.log('示例:');
    console.log('  node cli-anything-wrapper.js --wrap https://github.com');
    console.log('  node cli-anything-wrapper.js --execute ./cli-wrappers/github.json --command click-button-0');
  }
}

module.exports = CLIAnythingWrapper;
