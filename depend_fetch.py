import urllib.request
import urllib.error


class DependencyFetcher:
    def __init__(self, config):
        self.config = config
    
    def get_dependencies(self, package_name: str) -> list:
        if self.config.test_mode:
            from graph import TestRepository
            test_repo = TestRepository(self.config.test_repository_path)
            return test_repo.get_dependencies(package_name)
        else:
            return self.get_dependencies_from_github(package_name)
    
    def get_dependencies_from_github(self, package_name: str) -> list:
        repo_url = self.config.repository_url
        
        if repo_url.startswith('https://github.com/'):
            for branch in ['main', 'master']:
                raw_url = repo_url.replace('https://github.com/', 'https://raw.githubusercontent.com/')
                raw_url = raw_url.rstrip('/')
                raw_url += f'/{branch}/{package_name}/Cargo.toml'
                
                try:
                    with urllib.request.urlopen(raw_url, timeout=10) as response:
                        cargo_content = response.read().decode('utf-8')
                        return self.parse_dependencies(cargo_content)
                except urllib.error.HTTPError:
                    continue
                except urllib.error.URLError:
                    continue
            
            return []
        else:
            return []
    
    def parse_dependencies(self, cargo_toml_content: str) -> list:
        #Парсит Cargo.toml + зависимости
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
            if in_dependencies and line and not line.startswith('#') and '=' in line:
                dep_name = line.split('=')[0].strip()
                if dep_name:
                    dependencies.append(dep_name)
        
        return dependencies