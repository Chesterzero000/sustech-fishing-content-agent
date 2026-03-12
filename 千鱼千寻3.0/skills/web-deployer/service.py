"""
Web Deployer Service
自动化 Web 应用部署服务
"""
import os
import subprocess
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import paramiko
from pathlib import Path

logger = logging.getLogger(__name__)


class WebDeployerService:
    """Web 部署服务"""

    def __init__(self):
        """初始化服务"""
        self.server_host = os.getenv('DEPLOY_SERVER_HOST')
        self.server_user = os.getenv('DEPLOY_SERVER_USER', 'root')
        self.ssh_key_path = os.getenv('DEPLOY_SSH_KEY')
        self.deploy_path = os.getenv('DEPLOY_PATH', '/var/www/qianyu')

        if not self.server_host:
            raise ValueError("DEPLOY_SERVER_HOST environment variable is required")

        logger.info(f"Web Deployer initialized for {self.server_user}@{self.server_host}")

    def _get_ssh_client(self) -> paramiko.SSHClient:
        """获取 SSH 客户端"""
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if self.ssh_key_path:
            client.connect(
                self.server_host,
                username=self.server_user,
                key_filename=self.ssh_key_path
            )
        else:
            password = os.getenv('DEPLOY_SERVER_PASSWORD')
            client.connect(
                self.server_host,
                username=self.server_user,
                password=password
            )

        return client

    def _execute_remote_command(self, command: str) -> tuple:
        """执行远程命令"""
        try:
            client = self._get_ssh_client()
            stdin, stdout, stderr = client.exec_command(command)
            output = stdout.read().decode()
            error = stderr.read().decode()
            exit_code = stdout.channel.recv_exit_status()
            client.close()
            return exit_code, output, error
        except Exception as e:
            logger.error(f"Error executing remote command: {e}")
            return 1, "", str(e)

    def build_project(self, project_path: str, build_command: str = "npm run build") -> Dict[str, Any]:
        """
        构建项目

        Args:
            project_path: 项目路径
            build_command: 构建命令

        Returns:
            构建结果
        """
        try:
            logger.info(f"Building project at {project_path}")
            start_time = datetime.now()

            # 执行构建命令
            result = subprocess.run(
                build_command,
                shell=True,
                cwd=project_path,
                capture_output=True,
                text=True
            )

            build_time = (datetime.now() - start_time).total_seconds()

            if result.returncode == 0:
                return {
                    "success": True,
                    "data": {
                        "build_time": f"{build_time:.2f}s",
                        "output": result.stdout
                    }
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr
                }

        except Exception as e:
            logger.error(f"Error building project: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def deploy_init(
        self,
        project_path: str,
        domain: str,
        build_command: str = "npm run build",
        dist_dir: str = "dist"
    ) -> Dict[str, Any]:
        """
        首次部署

        Args:
            project_path: 项目路径
            domain: 域名
            build_command: 构建命令
            dist_dir: 构建输出目录

        Returns:
            部署结果
        """
        try:
            deployment_id = f"deploy_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            logger.info(f"Starting initial deployment: {deployment_id}")

            # 1. 构建项目
            build_result = self.build_project(project_path, build_command)
            if not build_result['success']:
                return build_result

            # 2. 创建部署目录
            deploy_dir = f"{self.deploy_path}/{deployment_id}"
            exit_code, _, error = self._execute_remote_command(f"mkdir -p {deploy_dir}")
            if exit_code != 0:
                return {"success": False, "error": f"Failed to create deploy directory: {error}"}

            # 3. 上传文件
            dist_path = os.path.join(project_path, dist_dir)
            rsync_command = f"rsync -avz --delete {dist_path}/ {self.server_user}@{self.server_host}:{deploy_dir}/"

            if self.ssh_key_path:
                rsync_command += f" -e 'ssh -i {self.ssh_key_path}'"

            result = subprocess.run(rsync_command, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                return {"success": False, "error": f"Failed to upload files: {result.stderr}"}

            # 4. 创建符号链接
            exit_code, _, error = self._execute_remote_command(
                f"ln -sfn {deploy_dir} {self.deploy_path}/current"
            )
            if exit_code != 0:
                return {"success": False, "error": f"Failed to create symlink: {error}"}

            # 5. 配置 Nginx
            nginx_result = self._configure_nginx_for_domain(domain)
            if not nginx_result['success']:
                logger.warning(f"Nginx configuration failed: {nginx_result.get('error')}")

            return {
                "success": True,
                "data": {
                    "deployment_id": deployment_id,
                    "status": "deployed",
                    "url": f"https://{domain}",
                    "build_time": build_result['data']['build_time'],
                    "deploy_time": "completed"
                }
            }

        except Exception as e:
            logger.error(f"Error in initial deployment: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def deploy_update(
        self,
        project_path: str,
        build_command: str = "npm run build",
        skip_build: bool = False
    ) -> Dict[str, Any]:
        """
        更新部署

        Args:
            project_path: 项目路径
            build_command: 构建命令
            skip_build: 跳过构建

        Returns:
            部署结果
        """
        try:
            deployment_id = f"deploy_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            logger.info(f"Starting update deployment: {deployment_id}")

            # 获取当前版本
            exit_code, current_version, _ = self._execute_remote_command(
                f"readlink {self.deploy_path}/current"
            )
            current_version = current_version.strip().split('/')[-1] if exit_code == 0 else "unknown"

            # 构建项目
            if not skip_build:
                build_result = self.build_project(project_path, build_command)
                if not build_result['success']:
                    return build_result

            # 部署新版本
            deploy_result = self.deploy_init(project_path, os.getenv('DEPLOY_DOMAIN', 'localhost'))

            if deploy_result['success']:
                deploy_result['data']['previous_version'] = current_version

            return deploy_result

        except Exception as e:
            logger.error(f"Error in update deployment: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def deploy_rollback(self, version: Optional[str] = None) -> Dict[str, Any]:
        """
        回滚部署

        Args:
            version: 回滚到指定版本（默认上一版本）

        Returns:
            回滚结果
        """
        try:
            logger.info(f"Rolling back deployment to version: {version or 'previous'}")

            # 获取当前版本
            exit_code, current_version, _ = self._execute_remote_command(
                f"readlink {self.deploy_path}/current"
            )
            current_version = current_version.strip().split('/')[-1]

            # 获取所有版本
            exit_code, versions_output, _ = self._execute_remote_command(
                f"ls -t {self.deploy_path} | grep deploy_"
            )
            versions = versions_output.strip().split('\n')

            if not version:
                # 回滚到上一版本
                if len(versions) < 2:
                    return {"success": False, "error": "No previous version found"}
                version = versions[1]

            # 执行回滚
            target_path = f"{self.deploy_path}/{version}"
            exit_code, _, error = self._execute_remote_command(
                f"ln -sfn {target_path} {self.deploy_path}/current"
            )

            if exit_code != 0:
                return {"success": False, "error": f"Failed to rollback: {error}"}

            return {
                "success": True,
                "data": {
                    "current_version": version,
                    "previous_version": current_version,
                    "status": "rolled_back"
                }
            }

        except Exception as e:
            logger.error(f"Error in rollback: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def deploy_status(self) -> Dict[str, Any]:
        """
        查看部署状态

        Returns:
            部署状态
        """
        try:
            # 获取当前版本
            exit_code, current_version, _ = self._execute_remote_command(
                f"readlink {self.deploy_path}/current"
            )
            current_version = current_version.strip().split('/')[-1] if exit_code == 0 else "unknown"

            # 检查服务状态
            domain = os.getenv('DEPLOY_DOMAIN', 'localhost')
            health_status = self._check_health(f"https://{domain}")

            return {
                "success": True,
                "data": {
                    "current_version": current_version,
                    "deployed_at": "N/A",
                    "url": f"https://{domain}",
                    "health_status": health_status,
                    "ssl_status": "N/A"
                }
            }

        except Exception as e:
            logger.error(f"Error getting deployment status: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def configure_ssl(
        self,
        domain: str,
        email: str,
        force_renew: bool = False
    ) -> Dict[str, Any]:
        """
        配置 SSL 证书

        Args:
            domain: 域名
            email: 邮箱
            force_renew: 强制续期

        Returns:
            配置结果
        """
        try:
            logger.info(f"Configuring SSL for {domain}")

            # 使用 certbot 申请证书
            certbot_command = f"certbot certonly --nginx -d {domain} --email {email} --agree-tos --non-interactive"
            if force_renew:
                certbot_command += " --force-renewal"

            exit_code, output, error = self._execute_remote_command(certbot_command)

            if exit_code != 0:
                return {"success": False, "error": f"Failed to configure SSL: {error}"}

            return {
                "success": True,
                "data": {
                    "domain": domain,
                    "status": "configured",
                    "issuer": "Let's Encrypt"
                }
            }

        except Exception as e:
            logger.error(f"Error configuring SSL: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def _configure_nginx_for_domain(self, domain: str) -> Dict[str, Any]:
        """配置 Nginx"""
        nginx_config = f"""
server {{
    listen 80;
    server_name {domain};
    return 301 https://$server_name$request_uri;
}}

server {{
    listen 443 ssl http2;
    server_name {domain};

    ssl_certificate /etc/letsencrypt/live/{domain}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/{domain}/privkey.pem;

    root {self.deploy_path}/current;
    index index.html;

    location / {{
        try_files $uri $uri/ /index.html;
    }}

    location /api {{
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }}
}}
"""
        # 写入配置文件
        config_path = f"/etc/nginx/sites-available/{domain}"
        exit_code, _, error = self._execute_remote_command(
            f"echo '{nginx_config}' > {config_path}"
        )

        if exit_code != 0:
            return {"success": False, "error": error}

        # 创建符号链接
        self._execute_remote_command(
            f"ln -sf {config_path} /etc/nginx/sites-enabled/{domain}"
        )

        # 测试配置
        exit_code, _, error = self._execute_remote_command("nginx -t")
        if exit_code != 0:
            return {"success": False, "error": f"Nginx config test failed: {error}"}

        # 重载 Nginx
        self._execute_remote_command("systemctl reload nginx")

        return {"success": True}

    def _check_health(self, url: str) -> str:
        """检查服务健康状态"""
        try:
            import requests
            response = requests.get(url, timeout=10)
            return "healthy" if response.status_code == 200 else "unhealthy"
        except Exception:
            return "unreachable"
