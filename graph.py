from collections import deque


class DependencyGraph:
    def __init__(self):
        self.graph = {}
        
    def build_graph_bfs(self, start_package: str, dependency_fetcher) -> dict:
        #Строит граф зависимостей используя BFS без рекурсии
        self.graph = {}
        visited = set()
        queue = deque([start_package])
        
        while queue:
            current_package = queue.popleft()
            
            if current_package in visited:
                continue
                
            visited.add(current_package)
            
            dependencies = dependency_fetcher.get_dependencies(current_package)
            self.graph[current_package] = dependencies
            
            for dep in dependencies:
                if dep not in visited and dep not in queue:
                    queue.append(dep)
        
        return self.graph
    
    def detect_cycles(self) -> list:
        cycles = []
        visited = set()
        recursion_stack = set()
        path = []
        
        def dfs(node: str):
            if node in recursion_stack:
                cycle_start = path.index(node)
                cycle = path[cycle_start:]
                if cycle not in cycles:
                    cycles.append(cycle)
                return
                
            if node in visited:
                return
                
            visited.add(node)
            recursion_stack.add(node)
            path.append(node)
            
            for neighbor in self.graph.get(node, []):
                dfs(neighbor)
                
            path.pop()
            recursion_stack.remove(node)
        
        for node in self.graph:
            if node not in visited:
                dfs(node)
                
        return cycles


class TestRepository:
    
    def __init__(self, test_file_path: str):
        self.test_file_path = test_file_path
        self.test_graph = self.load_test_graph()
    
    def load_test_graph(self) -> dict:
        test_graph = {}
        try:
            with open(self.test_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if ':' in line:
                        package, deps_str = line.split(':', 1)
                        package = package.strip()
                        dependencies = [d.strip() for d in deps_str.split() if d.strip()]
                        test_graph[package] = dependencies
        except Exception as e:
            raise Exception(f"Failed to load test repository: {e}")
        return test_graph
    
    def get_dependencies(self, package: str) -> list:
        return self.test_graph.get(package, [])