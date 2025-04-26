from typing import Any, Union

from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(loader=PackageLoader('src', 'templates'), autoescape=select_autoescape())


async def render(
    template_name: str,
    **kwargs: Union[int, str, dict[str, Any]],
) -> str:
    if not template_name.endswith('.jinja2'):
        template_name = f'{template_name}.jinja2'
    rendered_template = env.get_template(template_name).render(**kwargs)
    return rendered_template.format()
