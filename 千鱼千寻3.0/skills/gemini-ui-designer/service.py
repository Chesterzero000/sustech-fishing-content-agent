"""
Gemini UI Designer Service
使用 Google Gemini API 生成 UI 设计和图标
"""
import os
import json
import logging
from typing import Dict, List, Optional, Any
import google.generativeai as genai

logger = logging.getLogger(__name__)


class GeminiUIDesignerService:
    """Gemini UI 设计服务"""

    def __init__(self):
        """初始化服务"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")

        genai.configure(api_key=self.api_key)
        self.model_name = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash-exp')
        self.model = genai.GenerativeModel(self.model_name)

        logger.info(f"Gemini UI Designer initialized with model: {self.model_name}")

    def design_page_ui(
        self,
        page_name: str,
        description: str,
        style: str = "现代简约",
        color_scheme: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        生成页面 UI 设计

        Args:
            page_name: 页面名称
            description: 页面功能描述
            style: 设计风格
            color_scheme: 配色方案

        Returns:
            设计结果
        """
        try:
            prompt = f"""
你是一位专业的 UI/UX 设计师，请为以下小程序页面设计 UI：

页面名称：{page_name}
功能描述：{description}
设计风格：{style}
配色方案：{color_scheme or '请推荐合适的配色'}

请提供：
1. 页面布局建议（详细描述各区域的位置和功能）
2. 主要组件列表（如导航栏、卡片、按钮等）
3. 配色方案（主色、辅色、背景色、文字色）
4. 交互设计建议
5. 响应式设计考虑

请以 JSON 格式返回，包含以下字段：
- design_description: 整体设计描述
- layout: 布局详细说明
- components: 组件列表（数组）
- colors: 配色方案对象
- interactions: 交互设计建议
- responsive: 响应式设计建议
"""

            response = self.model.generate_content(prompt)
            result_text = response.text

            # 尝试解析 JSON
            try:
                # 提取 JSON 部分
                if '```json' in result_text:
                    json_start = result_text.find('```json') + 7
                    json_end = result_text.find('```', json_start)
                    result_text = result_text[json_start:json_end].strip()
                elif '```' in result_text:
                    json_start = result_text.find('```') + 3
                    json_end = result_text.find('```', json_start)
                    result_text = result_text[json_start:json_end].strip()

                design_data = json.loads(result_text)
            except json.JSONDecodeError:
                # 如果无法解析 JSON，返回原始文本
                design_data = {
                    "design_description": result_text,
                    "layout": "请查看设计描述",
                    "components": [],
                    "colors": {},
                    "interactions": "",
                    "responsive": ""
                }

            return {
                "success": True,
                "data": design_data
            }

        except Exception as e:
            logger.error(f"Error designing page UI: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def design_icon(
        self,
        icon_name: str,
        style: str = "扁平化",
        color: str = "#1890ff",
        format: str = "svg"
    ) -> Dict[str, Any]:
        """
        生成图标设计

        Args:
            icon_name: 图标名称
            style: 设计风格
            color: 主色调
            format: 输出格式

        Returns:
            图标设计结果
        """
        try:
            prompt = f"""
你是一位专业的图标设计师，请为以下功能设计图标：

图标名称：{icon_name}
设计风格：{style}
主色调：{color}
输出格式：{format}

请提供：
1. 图标设计理念
2. SVG 代码（如果适用）
3. 设计说明

请以 JSON 格式返回，包含以下字段：
- concept: 设计理念
- svg_code: SVG 代码（如果是 SVG 格式）
- description: 设计说明
- alternative_designs: 备选设计建议（数组）
"""

            response = self.model.generate_content(prompt)
            result_text = response.text

            # 尝试解析 JSON
            try:
                if '```json' in result_text:
                    json_start = result_text.find('```json') + 7
                    json_end = result_text.find('```', json_start)
                    result_text = result_text[json_start:json_end].strip()

                icon_data = json.loads(result_text)
            except json.JSONDecodeError:
                icon_data = {
                    "concept": result_text,
                    "svg_code": "",
                    "description": result_text,
                    "alternative_designs": []
                }

            return {
                "success": True,
                "data": icon_data
            }

        except Exception as e:
            logger.error(f"Error designing icon: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def generate_color_scheme(
        self,
        theme: str,
        mood: str,
        count: int = 5
    ) -> Dict[str, Any]:
        """
        生成配色方案

        Args:
            theme: 主题
            mood: 情绪/氛围
            count: 颜色数量

        Returns:
            配色方案
        """
        try:
            prompt = f"""
你是一位专业的色彩设计师，请为以下主题生成配色方案：

主题：{theme}
氛围：{mood}
颜色数量：{count}

请提供：
1. 主色（primary）
2. 辅色（secondary）
3. 强调色（accent）
4. 背景色（background）
5. 文字色（text）
6. 完整调色板（{count} 个颜色）
7. 配色说明

请以 JSON 格式返回，包含以下字段：
- primary: 主色（HEX）
- secondary: 辅色（HEX）
- accent: 强调色（HEX）
- background: 背景色（HEX）
- text: 文字色（HEX）
- palette: 完整调色板（数组）
- description: 配色说明
- usage_guide: 使用指南
"""

            response = self.model.generate_content(prompt)
            result_text = response.text

            # 尝试解析 JSON
            try:
                if '```json' in result_text:
                    json_start = result_text.find('```json') + 7
                    json_end = result_text.find('```', json_start)
                    result_text = result_text[json_start:json_end].strip()

                color_data = json.loads(result_text)
            except json.JSONDecodeError:
                color_data = {
                    "primary": "#1890ff",
                    "secondary": "#52c41a",
                    "accent": "#faad14",
                    "background": "#f0f2f5",
                    "text": "#262626",
                    "palette": [],
                    "description": result_text,
                    "usage_guide": ""
                }

            return {
                "success": True,
                "data": color_data
            }

        except Exception as e:
            logger.error(f"Error generating color scheme: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def design_complete_kit(
        self,
        app_name: str,
        pages: List[str],
        style: str = "现代简约",
        brand_keywords: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        生成完整 UI 设计套件

        Args:
            app_name: 应用名称
            pages: 页面列表
            style: 整体风格
            brand_keywords: 品牌关键词

        Returns:
            完整设计套件
        """
        try:
            keywords_str = ", ".join(brand_keywords) if brand_keywords else "无"
            pages_str = ", ".join(pages)

            prompt = f"""
你是一位资深的 UI/UX 设计总监，请为以下小程序设计完整的 UI 套件：

应用名称：{app_name}
页面列表：{pages_str}
设计风格：{style}
品牌关键词：{keywords_str}

请提供：
1. 品牌设计（Logo 理念、配色、字体）
2. 每个页面的设计方案
3. 图标系统
4. 设计规范文档

请以 JSON 格式返回，包含以下字段：
- brand: 品牌设计对象
  - logo_concept: Logo 设计理念
  - colors: 品牌配色
  - typography: 字体系统
- pages: 页面设计数组
  - name: 页面名称
  - design: 设计方案
  - components: 组件列表
- icons: 图标系统对象
- guidelines: 设计规范文档
"""

            response = self.model.generate_content(prompt)
            result_text = response.text

            # 尝试解析 JSON
            try:
                if '```json' in result_text:
                    json_start = result_text.find('```json') + 7
                    json_end = result_text.find('```', json_start)
                    result_text = result_text[json_start:json_end].strip()

                kit_data = json.loads(result_text)
            except json.JSONDecodeError:
                kit_data = {
                    "brand": {},
                    "pages": [],
                    "icons": {},
                    "guidelines": result_text
                }

            return {
                "success": True,
                "data": kit_data
            }

        except Exception as e:
            logger.error(f"Error designing complete kit: {e}")
            return {
                "success": False,
                "error": str(e)
            }
