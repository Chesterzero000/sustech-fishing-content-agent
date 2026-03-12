"""
Web Deployer CLI
"""
import click
from .service import WebDeployerService


@click.group()
def deploy():
    """Web 部署工具"""
    pass


@deploy.command()
@click.option('--project-path', required=True, help='项目路径')
@click.option('--domain', required=True, help='域名')
@click.option('--server', required=True, help='服务器地址 (user@host)')
@click.option('--build-command', default='npm run build', help='构建命令')
@click.option('--dist-dir', default='dist', help='构建输出目录')
def init(project_path, domain, server, build_command, dist_dir):
    """首次部署 Web 应用"""
    service = WebDeployerService()
    result = service.deploy_init(project_path, domain, build_command, dist_dir)

    if result['success']:
        data = result['data']
        click.echo(f"\n✅ 部署成功！")
        click.echo(f"部署 ID: {data['deployment_id']}")
        click.echo(f"访问地址: {data['url']}")
        click.echo(f"构建时间: {data['build_time']}")
    else:
        click.echo(f"❌ 部署失败: {result.get('error')}")


@deploy.command()
@click.option('--project-path', required=True, help='项目路径')
@click.option('--build-command', default='npm run build', help='构建命令')
@click.option('--skip-build', is_flag=True, help='跳过构建')
def update(project_path, build_command, skip_build):
    """更新部署"""
    service = WebDeployerService()
    result = service.deploy_update(project_path, build_command, skip_build)

    if result['success']:
        data = result['data']
        click.echo(f"\n✅ 更新成功！")
        click.echo(f"新版本: {data['deployment_id']}")
        click.echo(f"旧版本: {data.get('previous_version', 'N/A')}")
    else:
        click.echo(f"❌ 更新失败: {result.get('error')}")


@deploy.command()
@click.option('--version', help='回滚到指定版本（默认上一版本）')
def rollback(version):
    """回滚部署"""
    service = WebDeployerService()
    result = service.deploy_rollback(version)

    if result['success']:
        data = result['data']
        click.echo(f"\n✅ 回滚成功！")
        click.echo(f"当前版本: {data['current_version']}")
        click.echo(f"之前版本: {data['previous_version']}")
    else:
        click.echo(f"❌ 回滚失败: {result.get('error')}")


@deploy.command()
def status():
    """查看部署状态"""
    service = WebDeployerService()
    result = service.deploy_status()

    if result['success']:
        data = result['data']
        click.echo(f"\n📊 部署状态")
        click.echo(f"当前版本: {data['current_version']}")
        click.echo(f"访问地址: {data['url']}")
        click.echo(f"健康状态: {data['health_status']}")
        click.echo(f"SSL 状态: {data['ssl_status']}")
    else:
        click.echo(f"❌ 获取状态失败: {result.get('error')}")


@deploy.command()
@click.option('--domain', required=True, help='域名')
@click.option('--email', required=True, help='邮箱')
@click.option('--force-renew', is_flag=True, help='强制续期')
def ssl(domain, email, force_renew):
    """配置 SSL 证书"""
    service = WebDeployerService()
    result = service.configure_ssl(domain, email, force_renew)

    if result['success']:
        data = result['data']
        click.echo(f"\n✅ SSL 配置成功！")
        click.echo(f"域名: {data['domain']}")
        click.echo(f"状态: {data['status']}")
        click.echo(f"颁发者: {data['issuer']}")
    else:
        click.echo(f"❌ SSL 配置失败: {result.get('error')}")
