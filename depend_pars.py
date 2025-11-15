import urllib.request
import urllib.error


class DependencyParser:
    def __init__(self, config):
        self.config = config

    def get_cargo_toml_from_github(self, repo_url: str) -> str:
        if repo_url.startswith('https://github.com/'):
            branches = ['main', 'master']
            
            for branch in branches:
                raw_url = repo_url.replace('https://github.com/', 'https://raw.githubusercontent.com/')
                raw_url = raw_url.rstrip('/')
                raw_url += f'/{branch}/{self.config.package_name}/Cargo.toml'
                
                try:
                    with urllib.request.urlopen(raw_url, timeout=10) as response:
                        return response.read().decode('utf-8')
                except urllib.error.HTTPError:
                    raw_url_root = repo_url.replace('https://github.com/', 'https://raw.githubusercontent.com/')
                    raw_url_root = raw_url_root.rstrip('/') + f'/{branch}/Cargo.toml'
                    try:
                        with urllib.request.urlopen(raw_url_root, timeout=10) as response:
                            return response.read().decode('utf-8')
                    except urllib.error.HTTPError:
                        continue
                except urllib.error.URLError as e:
                    raise DependencyError(f"Failed to download Cargo.toml: {e}")
            
            raise DependencyError("Cargo.toml not found")
        else:
            raise DependencyError("Unsupported repository URL")

    def parse_dependencies(self, cargo_toml_content: str) -> list:
        dependencies = []
        lines = cargo_toml_content.split('\n')
        
        in_dependencies = False
        
        for line in lines:
            line = line.strip()
            
            if line == '[dependencies]':
                in_dependencies = True
                continue
            elif line.startswith('[') and in_dependencies:
                break
                
            if in_dependencies and line and not line.startswith('#'):
                line = line.split('#')[0].strip()
                if line and '=' in line:
                    dep_name = line.split('=')[0].strip()
                    if dep_name:
                        dependencies.append(dep_name)
        
        return dependencies

    def get_direct_dependencies(self) -> list:
        if self.config.test_mode:
            raise DependencyError("Test mode not implemented in stage 2")
        
        cargo_toml_content = self.get_cargo_toml_from_github(self.config.repository_url)
        return self.parse_dependencies(cargo_toml_content)


class DependencyError(Exception):
    pass