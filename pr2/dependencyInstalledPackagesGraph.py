import importlib.util
import sys

def get_module_dependencies(module_name):
    dependencies = set()
    try:
        module = importlib.import_module(module_name)
    except ImportError:
        return dependencies

    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, type(sys)):
            dependencies.add(obj.__name__)

    return dependencies

def generate_dependency_graph(package_name):
    graph = ['digraph dependencies {']
    visited = set()

    def traverse_dependencies(package):
        if package in visited:
            return
        visited.add(package)

        dependencies = get_module_dependencies(package)
        for dependency in dependencies:
            graph.append(f'  "{package}" -> "{dependency}";')
            traverse_dependencies(dependency)

    traverse_dependencies(package_name)
    graph.append('}')

    return '\n'.join(graph)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python dependencyInstalledPackagesGraph.py <package_name>')
        sys.exit(1)

    package_name = sys.argv[1]
    graph = generate_dependency_graph(package_name)
    print(graph)
