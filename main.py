#!/usr/bin/env python3
import sys
import os
from config import Config, ConfigError
from depend_pars import DependencyParser
from graph import DependencyGraph
from depend_fetch import DependencyFetcher


def print_config_as_key_value(config: Config) -> None:
    config_dict = config.to_dict()
    print("Configuration parameters:")
    for key, value in config_dict.items():
        print(f"  {key}: {value}")


def main():
    config_file = "config.json"
    
    if not os.path.exists(config_file):
        print(f"Error: Config file '{config_file}' not found.")
        sys.exit(1)

    try:
        config = Config.load_from_file(config_file)
        config.validate()
        
        print_config_as_key_value(config)
        
        
        if not config.test_mode:
            parser = DependencyParser(config)
            direct_dependencies = parser.get_direct_dependencies()
            print("Direct dependencies:")
            for dep in direct_dependencies:
                print(f"  - {dep}")
        
        #Полный граф BFS
        print("STAGE 3: Full Graph (BFS)")
        
        dependency_fetcher = DependencyFetcher(config)
        graph = DependencyGraph()
        
        full_graph = graph.build_graph_bfs(config.package_name, dependency_fetcher)
        
        print("Dependency graph:")
        for package, deps in full_graph.items():
            print(f"  {package}: {deps}")
        
        cycles = graph.detect_cycles()
        if cycles:
            print(f"\nCyclic dependencies found: {len(cycles)}")
            for cycle in cycles:
                print(f"  Cycle: {' -> '.join(cycle)}")
        else:
            print("\nNo cyclic dependencies found")
        
        print("\nStage 3 completed successfully!")
        
    except ConfigError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()