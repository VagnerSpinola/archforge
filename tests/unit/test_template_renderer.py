from archforge.services.template_renderer import TemplateRenderer


def test_template_renderer_renders_common_entity_template() -> None:
    renderer = TemplateRenderer()

    output = renderer.render(
        "common/entity.py.j2",
        {"class_name": "Invoice", "module_name": "invoice", "project_name": "billing-service"},
    )

    assert "class Invoice" in output