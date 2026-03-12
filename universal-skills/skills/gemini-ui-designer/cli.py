"""
Gemini UI Designer CLI
"""
import click
from .service import GeminiUIDesignerService


@click.group()
def ui():
    """UI 设计工具"""
    pass


@ui.command()
@click.option('--name', required=True, help='页面名称')
@click.option('--description', required=True, help='页面功能描述')
@click.option('--style', default='现代简约', help='设计风格')
@click.option('--color-scheme', help='配色方案')
def design_page(name, description, style, color_scheme):
    """生成页面 UI 设计"""
    service = GeminiUIDesignerService()
    result = service.design_page_ui(name, description, style, color_scheme)

    if result['success']:
        click.echo(f"\n✅ 页面设计生成成功：{name}\n")
        data = result['data']
        click.echo(f"设计描述：{data.get('design_description', '')}\n")
        click.echo(f"布局：{data.get('layout', '')}\n")
        click.echo(f"组件：{', '.join(data.get('components', []))}\n")
        if 'colors' in data:
            click.echo("配色方案：")
            for key, value in data['colors'].items():
                click.echo(f"  {key}: {value}")
    else:
        click.echo(f"❌ 生成失败：{result.get('error')}")


@ui.command()
@click.option('--name', required=True, help='图标名称')
@click.option('--style', default='扁平化', help='设计风格')
@click.option('--color', default='#1890ff', help='主色调')
@click.option('--format', default='svg', help='输出格式')
def design_icon(name, style, color, format):
    """生成图标设计"""
    service = GeminiUIDesignerService()
    result = service.design_icon(name, style, color, format)

    if result['success']:
        click.echo(f"\n✅ 图标设计生成成功：{name}\n")
        data = result['data']
        click.echo(f"设计理念：{data.get('concept', '')}\n")
        if 'svg_code' in data and data['svg_code']:
            click.echo("SVG 代码：")
            click.echo(data['svg_code'])
    else:
        click.echo(f"❌ 生成失败：{result.get('error')}")


@ui.command()
@click.option('--theme', required=True, help='主题')
@click.option('--mood', required=True, help='情绪/氛围')
@click.option('--count', default=5, help='颜色数量')
def color_scheme(theme, mood, count):
    """生成配色方案"""
    service = GeminiUIDesignerService()
    result = service.generate_color_scheme(theme, mood, count)

    if result['success']:
        click.echo(f"\n✅ 配色方案生成成功\n")
        data = result['data']
        click.echo(f"主色：{data.get('primary', '')}")
        click.echo(f"辅色：{data.get('secondary', '')}")
        click.echo(f"强调色：{data.get('accent', '')}")
        click.echo(f"背景色：{data.get('background', '')}")
        click.echo(f"文字色：{data.get('text', '')}")
        click.echo(f"\n调色板：{', '.join(data.get('palette', []))}")
        click.echo(f"\n说明：{data.get('description', '')}")
    else:
        click.echo(f"❌ 生成失败：{result.get('error')}")


@ui.command()
@click.option('--app-name', required=True, help='应用名称')
@click.option('--pages', required=True, help='页面列表（逗号分隔）')
@click.option('--style', default='现代简约', help='整体风格')
@click.option('--keywords', help='品牌关键词（逗号分隔）')
def design_kit(app_name, pages, style, keywords):
    """生成完整 UI 设计套件"""
    service = GeminiUIDesignerService()
    pages_list = [p.strip() for p in pages.split(',')]
    keywords_list = [k.strip() for k in keywords.split(',')] if keywords else None

    result = service.design_complete_kit(app_name, pages_list, style, keywords_list)

    if result['success']:
        click.echo(f"\n✅ UI 设计套件生成成功：{app_name}\n")
        data = result['data']

        if 'brand' in data:
            click.echo("品牌设计：")
            brand = data['brand']
            click.echo(f"  Logo 理念：{brand.get('logo_concept', '')}")

        if 'pages' in data:
            click.echo(f"\n页面设计（共 {len(data['pages'])} 个）：")
            for page in data['pages']:
                click.echo(f"  - {page.get('name', '')}")

        if 'guidelines' in data:
            click.echo(f"\n设计规范：\n{data['guidelines']}")
    else:
        click.echo(f"❌ 生成失败：{result.get('error')}")
