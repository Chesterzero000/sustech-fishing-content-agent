---
name: gemini-ui-designer
description: "使用 Gemini API 生成 UI 设计和图标，替代 emoji 表情"
metadata:
  {
    "openclaw": {
      "emoji": "🎨",
      "requires": {
        "env": ["GEMINI_API_KEY"]
      },
      "os": ["linux", "darwin", "win32"]
    }
  }
---

# Gemini UI Designer Skill

## 功能描述

使用 Google Gemini API 生成专业的 UI 设计和图标，包括：
- 小程序页面 UI 设计
- 图标和 Logo 设计
- 配色方案建议
- 布局和交互设计
- SVG 图标生成

## 使用场景

1. **页面设计**：根据功能需求生成小程序页面设计
2. **图标设计**：为功能模块生成专业图标
3. **品牌设计**：生成 Logo 和品牌视觉元素
4. **UI 优化**：对现有界面提供优化建议

## CLI 命令

```bash
# 生成页面 UI 设计
fishing-cli ui design-page --name "钓点地图" --description "显示附近钓点的地图页面"

# 生成图标
fishing-cli ui design-icon --name "渔获记录" --style "扁平化" --color "#1890ff"

# 生成配色方案
fishing-cli ui color-scheme --theme "钓鱼" --mood "平静、专业"

# 生成完整 UI 套件
fishing-cli ui design-kit --pages "首页,钓点,渔获,社区" --style "现代简约"
```

## MCP 工具

### 1. design_page_ui
生成页面 UI 设计

**参数**：
- `page_name` (string): 页面名称
- `description` (string): 页面功能描述
- `style` (string, optional): 设计风格（现代/简约/扁平/拟物）
- `color_scheme` (string, optional): 配色方案

**返回**：
```json
{
  "success": true,
  "data": {
    "design_description": "页面设计描述",
    "layout": "布局建议",
    "components": ["组件列表"],
    "colors": {
      "primary": "#1890ff",
      "secondary": "#52c41a"
    },
    "mockup_url": "设计稿 URL"
  }
}
```

### 2. design_icon
生成图标设计

**参数**：
- `icon_name` (string): 图标名称
- `style` (string): 设计风格
- `color` (string, optional): 主色调
- `format` (string, optional): 输出格式（svg/png）

**返回**：
```json
{
  "success": true,
  "data": {
    "svg_code": "<svg>...</svg>",
    "png_url": "图标 URL",
    "description": "图标设计说明"
  }
}
```

### 3. generate_color_scheme
生成配色方案

**参数**：
- `theme` (string): 主题
- `mood` (string): 情绪/氛围
- `count` (int, optional): 颜色数量

**返回**：
```json
{
  "success": true,
  "data": {
    "primary": "#1890ff",
    "secondary": "#52c41a",
    "accent": "#faad14",
    "background": "#f0f2f5",
    "text": "#262626",
    "palette": ["#color1", "#color2", "..."]
  }
}
```

### 4. design_complete_kit
生成完整 UI 设计套件

**参数**：
- `app_name` (string): 应用名称
- `pages` (array): 页面列表
- `style` (string): 整体风格
- `brand_keywords` (array, optional): 品牌关键词

**返回**：
```json
{
  "success": true,
  "data": {
    "brand": {
      "logo_url": "Logo URL",
      "colors": {},
      "typography": {}
    },
    "pages": [
      {
        "name": "首页",
        "design_url": "设计稿 URL",
        "components": []
      }
    ],
    "icons": {},
    "guidelines": "设计规范文档"
  }
}
```

## 技术实现

### API 调用
- 使用 Google Gemini API (gemini-2.0-flash-exp)
- 支持图像生成和设计建议
- 集成 Imagen 3 进行图标生成

### 输出格式
- SVG 矢量图标
- PNG 高清图片
- 设计规范文档（Markdown）
- Figma/Sketch 兼容格式

## 环境变量

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.0-flash-exp
IMAGEN_ENABLED=true
```

## 示例

### 生成钓点地图页面设计
```bash
fishing-cli ui design-page \
  --name "钓点地图" \
  --description "显示附近钓点，支持筛选和导航" \
  --style "现代简约" \
  --color-scheme "蓝绿色系"
```

### 生成渔获记录图标
```bash
fishing-cli ui design-icon \
  --name "渔获记录" \
  --style "扁平化" \
  --color "#1890ff" \
  --format "svg"
```

## 注意事项

1. 需要有效的 Gemini API Key
2. 图像生成可能需要较长时间
3. 建议批量生成以提高效率
4. 生成的设计需要人工审核和调整
