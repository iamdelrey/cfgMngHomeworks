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
        print('Usage: python dependency_graph.py <package_name>')
        sys.exit(1)

    package_name = sys.argv[1]
    graph = generate_dependency_graph(package_name)
    print(graph)

# import importlib.util
# import sys
#
# def get_module_dependencies(module_name):
#     dependencies = set()
#     visited_modules = set()
#
#     def traverse_dependencies(module_name):
#         if module_name in visited_modules:
#             return
#         visited_modules.add(module_name)
#
#         try:
#             spec = importlib.util.find_spec(module_name)
#             if spec is None:
#                 return
#
#             module = importlib.util.module_from_spec(spec)
#             spec.loader.exec_module(module)
#
#             for name, value in vars(module).items():
#                 if isinstance(value, type(sys)):
#                     if hasattr(value, '__module__'):
#                         dependencies.add(value.__module__)
#                     elif hasattr(value, '__name__'):
#                         dependencies.add(value.__name__)
#
#         except ImportError:
#             return
#
#     traverse_dependencies(module_name)
#     return dependencies
#
# def generate_dependency_graph(package_name):
#     graph = ['digraph dependencies {']
#     visited = set()
#
#     def traverse_dependencies(package):
#         if package in visited:
#             return
#         visited.add(package)
#
#         dependencies = get_module_dependencies(package)
#         for dependency in dependencies:
#             graph.append(f'  "{package}" -> "{dependency}";')
#             traverse_dependencies(dependency)
#
#     traverse_dependencies(package_name)
#     graph.append('}')
#
#     return '\n'.join(graph)
#
# if __name__ == '__main__':
#     if len(sys.argv) != 2:
#         print('Usage: python dependency_graph.py <package_name>')
#         sys.exit(1)
#
#     package_name = sys.argv[1]
#     graph = generate_dependency_graph(package_name)
#     print(graph)