"""V3 (comfy_api schema) wrappers for the StringEssentials nodes.

Import-guarded: if comfy_api is unavailable (older ComfyUI), this module exposes
nothing and the V1 NODE_CLASS_MAPPINGS in __init__.py remain the only path.

The wrappers are thin adapters. Each V3 node is built from the matching V1 class
by reading its INPUT_TYPES / RETURN_TYPES / RETURN_NAMES, and its execute()
delegates to the V1 class method, so the string logic is never forked.
"""

try:
    from comfy_api.v0_0_2 import io, ui, ComfyExtension
    _V3_AVAILABLE = True
except ImportError:
    _V3_AVAILABLE = False


if _V3_AVAILABLE:

    _OUT = {"STRING": io.String, "BOOLEAN": io.Boolean, "INT": io.Int}

    def _to_input(name, spec, optional):
        t = spec[0]
        opts = spec[1] if len(spec) > 1 else {}
        if isinstance(t, list):
            return io.Combo.Input(name, options=t, default=opts.get("default"),
                                  tooltip=opts.get("tooltip"), optional=optional)
        if t == "STRING":
            return io.String.Input(name, default=opts.get("default", ""),
                                   multiline=opts.get("multiline", False),
                                   placeholder=opts.get("placeholder"),
                                   tooltip=opts.get("tooltip"),
                                   force_input=opts.get("forceInput"), optional=optional)
        if t == "INT":
            return io.Int.Input(name, default=opts.get("default", 0), min=opts.get("min"),
                                max=opts.get("max"), step=opts.get("step"),
                                tooltip=opts.get("tooltip"), optional=optional)
        if t == "BOOLEAN":
            return io.Boolean.Input(name, default=opts.get("default", False),
                                    label_on=opts.get("label_on"), label_off=opts.get("label_off"),
                                    tooltip=opts.get("tooltip"), optional=optional)
        raise ValueError(f"StringEssentials V3: unmapped input type {t!r} for {name}")

    def _build_inputs(v1_cls):
        spec = v1_cls.INPUT_TYPES()
        inputs = []
        for section, optional in (("required", False), ("optional", True)):
            for name, s in spec.get(section, {}).items():
                inputs.append(_to_input(name, s, optional))
        return inputs

    def _build_outputs(v1_cls):
        names = getattr(v1_cls, "RETURN_NAMES", None) or v1_cls.RETURN_TYPES
        return [_OUT[t].Output(id=n, display_name=n)
                for t, n in zip(v1_cls.RETURN_TYPES, names)]

    def make_v3(node_id, display_name, v1_cls):
        func = v1_cls.FUNCTION
        is_output = getattr(v1_cls, "OUTPUT_NODE", False)
        desc = getattr(v1_cls, "DESCRIPTION", "")
        has_is_changed = hasattr(v1_cls, "IS_CHANGED")

        class _V3(io.ComfyNode):
            @classmethod
            def define_schema(cls):
                return io.Schema(
                    node_id=node_id,
                    display_name=display_name,
                    category=v1_cls.CATEGORY,
                    description=desc,
                    inputs=_build_inputs(v1_cls),
                    outputs=_build_outputs(v1_cls),
                    is_output_node=is_output,
                )

            @classmethod
            def execute(cls, **kwargs) -> io.NodeOutput:
                result = getattr(v1_cls(), func)(**kwargs)
                # OUTPUT_NODE preview returns {"ui": {"text": (...)}, "result": (...)}.
                if isinstance(result, dict):
                    text = result.get("ui", {}).get("text", [""])
                    res = result.get("result", ())
                    return io.NodeOutput(*res, ui=ui.PreviewText(text[0] if text else ""))
                return io.NodeOutput(*result)

        if has_is_changed:
            @classmethod
            def _fingerprint(cls, **kwargs):
                return v1_cls.IS_CHANGED(**kwargs)
            _V3.fingerprint_inputs = _fingerprint

        _V3.__name__ = node_id + "V3"
        return _V3

    class StringEssentialsExtension(ComfyExtension):
        async def get_node_list(self):
            # Imported at call time (after the package finished importing) to
            # avoid a circular import with __init__.py.
            from . import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
            return [make_v3(nid, NODE_DISPLAY_NAME_MAPPINGS.get(nid, nid), cls)
                    for nid, cls in NODE_CLASS_MAPPINGS.items()]

    async def comfy_entrypoint() -> "StringEssentialsExtension":
        return StringEssentialsExtension()
