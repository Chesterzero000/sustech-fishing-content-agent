const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

// 测试配置
const tests = [
  { name: 'GitHub', script: 'tests/logins/github.js' },
  { name: '小红书', script: 'tests/logins/xiaohongshu.js' },
  { name: '抖音', script: 'tests/logins/douyin.js' },
  { name: 'B站', script: 'tests/logins/bilibili.js' },
];

// 测试结果
const results = [];

console.log('🚀 开始批量测试所有平台');
console.log('==========================================');
console.log('');

// 运行单个测试
function runTest(test) {
  return new Promise((resolve) => {
    console.log(`📝 测试 ${test.name}...`);
    console.log(`   脚本: ${test.script}`);
    console.log('');

    const startTime = Date.now();
    const child = spawn('node', [test.script], {
      cwd: __dirname,
      stdio: 'inherit'
    });

    child.on('close', (code) => {
      const duration = ((Date.now() - startTime) / 1000).toFixed(2);
      const success = code === 0;

      results.push({
        name: test.name,
        script: test.script,
        success,
        code,
        duration
      });

      console.log('');
      console.log(`${success ? '✅' : '❌'} ${test.name} 测试${success ? '成功' : '失败'} (耗时: ${duration}秒)`);
      console.log('------------------------------------------');
      console.log('');

      resolve();
    });

    child.on('error', (error) => {
      console.error(`❌ 运行 ${test.name} 测试时出错:`, error.message);
      results.push({
        name: test.name,
        script: test.script,
        success: false,
        error: error.message,
        duration: 0
      });
      resolve();
    });
  });
}

// 依次运行所有测试
async function runAllTests() {
  for (const test of tests) {
    await runTest(test);
  }

  // 生成测试报告
  console.log('');
  console.log('==========================================');
  console.log('📊 测试报告');
  console.log('==========================================');
  console.log('');

  const successCount = results.filter(r => r.success).length;
  const failCount = results.filter(r => !r.success).length;
  const totalDuration = results.reduce((sum, r) => sum + parseFloat(r.duration || 0), 0).toFixed(2);

  console.log(`总测试数: ${results.length}`);
  console.log(`✅ 成功: ${successCount}`);
  console.log(`❌ 失败: ${failCount}`);
  console.log(`⏱️  总耗时: ${totalDuration}秒`);
  console.log('');

  console.log('详细结果:');
  console.log('------------------------------------------');
  results.forEach((result, index) => {
    const status = result.success ? '✅ 成功' : '❌ 失败';
    console.log(`${index + 1}. ${result.name}: ${status} (${result.duration}秒)`);
    if (result.error) {
      console.log(`   错误: ${result.error}`);
    }
  });
  console.log('');

  // 保存报告到文件
  const reportPath = path.join(__dirname, 'test-report.json');
  const reportData = {
    timestamp: new Date().toISOString(),
    summary: {
      total: results.length,
      success: successCount,
      failed: failCount,
      duration: totalDuration
    },
    results
  };

  fs.writeFileSync(reportPath, JSON.stringify(reportData, null, 2));
  console.log(`📄 测试报告已保存到: ${reportPath}`);

  // 生成文本报告
  const textReportPath = path.join(__dirname, 'test-report.txt');
  let textReport = '自动化测试报告\n';
  textReport += '==========================================\n\n';
  textReport += `测试时间: ${new Date().toLocaleString('zh-CN')}\n\n`;
  textReport += `总测试数: ${results.length}\n`;
  textReport += `成功: ${successCount}\n`;
  textReport += `失败: ${failCount}\n`;
  textReport += `总耗时: ${totalDuration}秒\n\n`;
  textReport += '详细结果:\n';
  textReport += '------------------------------------------\n';
  results.forEach((result, index) => {
    const status = result.success ? '✅ 成功' : '❌ 失败';
    textReport += `${index + 1}. ${result.name}: ${status} (${result.duration}秒)\n`;
    if (result.error) {
      textReport += `   错误: ${result.error}\n`;
    }
  });

  fs.writeFileSync(textReportPath, textReport);
  console.log(`📄 文本报告已保存到: ${textReportPath}`);
  console.log('');

  // 检查 Cookies
  console.log('==========================================');
  console.log('🍪 Cookies 状态检查');
  console.log('==========================================');
  console.log('');

  const cookiesDir = path.join(__dirname, 'cookies');
  if (fs.existsSync(cookiesDir)) {
    const cookieFiles = fs.readdirSync(cookiesDir).filter(f => f.endsWith('.json'));
    console.log(`找到 ${cookieFiles.length} 个 Cookies 文件:`);
    cookieFiles.forEach(file => {
      const filePath = path.join(cookiesDir, file);
      const stats = fs.statSync(filePath);
      const size = (stats.size / 1024).toFixed(2);
      const modified = stats.mtime.toLocaleString('zh-CN');
      console.log(`  - ${file} (${size}KB, 修改时间: ${modified})`);
    });
  } else {
    console.log('⚠️  Cookies 目录不存在');
  }

  console.log('');
  console.log('✅ 所有测试完成！');
}

// 开始运行
runAllTests().catch(error => {
  console.error('❌ 运行测试时出错:', error);
  process.exit(1);
});
